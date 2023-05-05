from django.shortcuts import render
from django.contrib.auth.hashers import make_password

from .serializers import MovieSerializer,TheatreSerializer,ShowSerializer,SeatSerializer,TicketSerializer,PaymentSerializer,CustomerSerializer
from .models import Movie,Theatre,Show,Seat,Ticket,Payment,Customer
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,get_user_model
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from django.contrib.auth.models import User,update_last_login
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated,AllowAny
from django.contrib.auth.tokens import default_token_generator
import pickle
import stripe

# Create your views here.
# def getPredictions(movie_name,movies):
#     model=pickle.load(open('recommender_model.sav','rb'))
#     prediction=model.predict([
#         movies['title']
#     ])
#     if prediction ==0:
#         return 'no similar movies'
#     else:
#         return {'movies':movie_name}    

class CustomPagination(PageNumberPagination):
    page_size=10
    page_query_param='page_size'
    max_page_size=100


class MovieVIewSet(viewsets.ModelViewSet):
    # def get_object(self,request):
    #     movie_name=int(request.GET('title'))
    #     result=getPredictions(movie_name)
    #     return result
    
    queryset=Movie.objects.all()
    serializer_class=MovieSerializer

    permission_classes=[IsAuthenticatedOrReadOnly]
    pagination_class=CustomPagination


    # def get_serializer_context(self):
    #     context=super(MovieVIewSet,self).get_serializer_context()
    #     context.update({'request':self.request.result})
    #     return context

class TheatreViewSet(viewsets.ModelViewSet):
    serializer_class=TheatreSerializer
    queryset=Theatre.objects.all()

    permission_classes=[IsAuthenticatedOrReadOnly]
    pagination_class=CustomPagination

class ShowViewSet(viewsets.ModelViewSet):
    serializer_class=ShowSerializer
    queryset=Show.objects.all()
    
    permission_classes=[IsAuthenticatedOrReadOnly]
    pagination_class=CustomPagination

class SeatViewSet(viewsets.ModelViewSet):
    queryset=Seat.objects.all()
    serializer_class=SeatSerializer

    permission_classes=[IsAuthenticatedOrReadOnly]
    pagination_class=CustomPagination

    def retrieve(self, request, *args, **kwargs):
        instance=self.get_object()
        serializer=self.get_serializer(instance)
        data=serializer.data

        if instance.is_booked:
            data['status']='Booked'

        else:
            data['status']='Available'
    

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class=TicketSerializer
    queryset=Ticket.objects.all()

    permission_classes=[IsAuthenticatedOrReadOnly]
    pagination_class=CustomPagination

class PaymentViewSet(viewsets.ModelViewSet):
    queryset=Payment.objects.all()
    serializer_class=PaymentSerializer

    permission_classes=[IsAuthenticated]
    pagination_class=CustomPagination

    @action(detail=True,methods=['post'])
    def create_payment_intent(self,request,pk=None):
        movie=self.get_object()
        amount=request.data.get('amount')

        try:
            payment_intent=stripe.PaymentIntent.create(
                amount=amount,
                currency='NPR'
            )
            return Response({
                'message':payment_intent.client_secret
            })
        except stripe.error.StripeError as e:
            return Response({
                'error':str(e)
            },status=400)

    @action(detail=True,methods=['post'])
    def handle_payment_webhook(self,request,pk=None):
        movie=self.get_object()
        payload=request.body
        sig_header=request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event=stripe.Webhook.construct_event(payload,sig_header,settings.STRIPE_WEBHOOK_SECRET)

            if event['type']=='payment_intent.succeeded':
                payment_intent=event['data']['object']

            return Response({
                'status':'success'
            })
        except stripe.error.SignatureVerificationError as e:
            return Response({
                'error':'Invalid webhook signature'
            })
        except stripe.error.StripeError as e:
            return Response({
                'error':str(e)

            },status=400) 
    

## This is the Customer viewset using jwt authentication
class CustomerViewSet(viewsets.ModelViewSet):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer

    permission_classes_by_action={
        'create':[AllowAny],
        'login':[AllowAny],
        'change_password':[IsAuthenticated]
        }
    pagination_class=CustomPagination

    ## defining permission classes
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError as e:

            return [permission() for permission in self.permission_classes]




    ## This code is for creating new user or custoner with email and password entered by user

    def create(self,request,*args,**kwargs):
        email=request.data.get('email')
        password=request.data.get('password')

        user=authenticate(request,email=email,password=password)

        if user:
            refresh=RefreshToken.for_user(user)
            serializer=self.get_serializer(user)
            return Response({'token':str(refresh.access_token),'user':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid email or password'},status=status.HTTP_401_UNAUTHORIZED)
        

    ## This code is for updating password while user is logged in

    def update(self,request,*args,**kwargs):
        instance=self.get_object()
        current_password=request.data.get('current_password')
        new_pasword=request.data.get('new_password')

        if not instance.check_password(current_password):
            return Response({'error':'Invalid current password'},status=status.HTTP_400_BAD_REQUEST)
        

        instance.set_password(new_pasword)
        instance.save()
        update_last_login(None,instance)
        return Response({'message':'Password updated successfully'},status=status.HTTP_200_OK)
    
    ## this code is used for forget password
User=get_user_model
class ForgotPasswordViewSet(APIView):
        def post(self,request):
            email=request.data.get('email')
            try:
                user=User.objects.get(email=email)

            except User.DoesNotExist:
                return Response({'error':'User with this email does not exist'},status=status.HTTP_404_NOT_FOUND)
        
            token=default_token_generator.make_token(user)
            reset_link=f"{settings.FRONTEND_URL}/reset-password/?token={token}"
            message=f"Hi {user.username},\n\nPlease click the link below to reset your password:\n{reset_link}"
            send_mail('Reset Password',message,settings.EMAIL_HOST_USER,[email])
            return Response({'message':'Reset password link has been sent to your email'},status=status.HTTP_200_OK)
User=get_user_model    
class ResetPasswordViewSet(APIView):
    def post(self,request):
        token=request.data.get('token')
        password=request.data.get('password')

        try:
            user=User.objects.get(pk=token)

        except User.DoesNotExist:
            return Response({'error':'Invalid or expired token'},status=status.HTTP_400_BAD_REQUEST)
        

        user.set_password(password)
        user.save()
        return Response({'message':'Password reset successful please login to continue'},status=status.HTTP_200_OK)
    







# from rest_framework import status
# from rest_framework import generics
# from rest_framework.response import Response
# from django.contrib.auth.models import User
# from .serializers import ChangePasswordSerializer
# from rest_framework.permissions import IsAuthenticated

# class ChangepasswordView(generics.UpdateAPIView):
    
    # serializer_class=ChangePasswordSerializer
    # model=User
    # permission_classes=[IsAuthenticated]

    # def get_object(self,queryset=None):
    #     obj=self.request.user
    #     return obj

    # def update(self,request,*args,**kwargs):
    #     self.object=self.get_object()
    #     serializer=self.get_serializer(data=request.data)

    #     if serializer.is_valid():
    #         # check old Password
    #         if not self.object.check_password(serializer.data.get("old password")):
    #             return Response({"old password":["wrong password"]},status=status.HTTP_400_BAD_REQUEST)
    #         #set password also hashes tha password that user will get
    #         self.object.set_password(serializer.data.get("new password"))
    #         self.object.save()
    #         response={
    #             'status': 'success',
    #             'code': status.HTTP_200_OK,
    #             'message': 'Password updated successfully',
    #             'data': []
    #         }
    #         return Response(response)
    #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# from django.views.generic import View
# from django.shortcuts import redirect
# from django.contrib import messages
# from django.core.mail import send_mail, send_mass_mail

# class SendFormEmail(View):

#     def  get(self, request):

#         # Get the form data 
#         name = request.GET.get('name', None)
#         email = request.GET.get('email', None)
#         message = request.GET.get('message', None)

#         # Send Email
#         send_mail(
#             'Subject - Django Email Testing', 
#             'Hello ' + name + ',\n' + message, 
#             'sender@example.com', # Admin
#             [
#                 email,
#             ]
#         ) 

#         # Redirect to same page after form submit
#         messages.success(request, ('Email sent successfully.'))
#         return redirect('home') 

#         send_mail(
#             'subject', 
#             'body of the message', 
#             'sender@example.com', 
#             [
#                 'receiver1@example.com', 
#                 'receiver2@example.com'
#             ]
#         ) 
#         message1 = ('Subject here', 'Here is the message', 'from@example.com', ['first@example.com', 'other@example.com'])
#         message2 = ('Another Subject', 'Here is another message', 'from@example.com', ['second@test.com'])

#         send_mass_mail((message1, message2), fail_silently=False)
# # from rest_framework import generics, permissions
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token

# from .models import User
# from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer

# class ForgotPasswordView(generics.GenericAPIView):
#     serializer_class = ForgotPasswordSerializer
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data['email']

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({'error': 'The email address is not registered'}, status=400)

#         user.generate_forgot_password_token()
#         user.save()

#         # Send an email to the user with a password reset link
#         # ...

#         return Response({'message': 'A password reset email has been sent to your email address.'})

# class ResetPasswordView(generics.GenericAPIView):
#     serializer_class = ResetPasswordSerializer
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         token = serializer.validated_data['token']
#         password = serializer.validated_data['password']

#         user = User.objects.filter(forgot_password_token=token).first()
#         if not user:
#             return Response({'error': 'Invalid token'}, status=400)

#         user.set_password(password)
#         user.forgot_password_token = ''
#         user.save()

#         # Delete the existing token to prevent reuse
#         Token.objects.filter(user=user).delete()

# #         return Response({'message': 'Your password has been reset successfully.'})
# class ForgetPasswordView(viewsets.ViewSet):
#     serializer_class=ForgetPaswordSerializer
#     permission_classes=[]
    
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         token = serializer.validated_data['token']
#         password = serializer.validated_data['password']

#         user = User.objects.filter(forgot_password_token=token).first()
#         if not user:
#             return Response({'error': 'Invalid token'}, status=400)

#         user.set_password(password)
#         user.forgot_password_token = ''
#         user.save()

#         # Delete the existing token to prevent reuse
#         Token.objects.filter(user=user).delete()

#         return Response({'message': 'Your password has been reset successfully.'})


# from django.shortcuts import render
# from rest_framework import exceptions, generics, serializers
# from rest_framework.response import Response
# from rest_framework import status
# from .models import *
# from .serializers import *
# from rest_framework_simplejwt.tokens import RefreshToken
# from .utils import *
# from django.contrib.sites.shortcuts import get_current_site
# from django.urls import reverse
# import jwt
# from django.conf import settings
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# # Create your views here.
# class RegisterView(generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class=RegisterSerializer
#     def post(self, request):
#         user = request.data
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         user_data = serializer.data

#         user= User.objects.get(email=user_data['email'])
#         token=RefreshToken.for_user(user).access_token

#         current_site=get_current_site(request).domain
#         realtivelink = reverse('email-verify')
        
#         absurl='http://'+current_site+realtivelink+"?token="+ str(token)
#         email_body='Hi '+ user.email+ ' Use link below to verify your email \n' + absurl
#         data={'email_body':email_body,'to_email':user.email,'email_subject':'Verify your email'}
#         Util.send_email(data)
#         return Response(user_data,status= status.HTTP_201_CREATED)

# class VerifyEmail(generics.GenericAPIView):
#     def get(self,request):
#         token= request.GET.get('token')
#         try:
#             payload=jwt.decode(token,settings.SECRET_KEY,algorithms='HS256')
#             user=User.objects.get(id=payload['user_id'])

#             if not user.is_verified:
#                 user.is_verified=True
#                 user.save()
#             return Response({'email':'Successfully activated'},status= status.HTTP_200_OK)
#         except jwt.ExpiredSignatureError as indentifier:
#             return Response({'email':'Activation expired'},status= status.HTTP_400_BAD_REQUEST)
#         except jwt.exceptions.DecodeError as indentifier:
#             return Response({'email':'Invalid token'},status= status.HTTP_400_BAD_REQUEST)


# class LoginAPIView(generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = LoginSerializers
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data,status=status.HTTP_200_OK )

# class RequestPasswordResetEmail(generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class=ResetPasswordViaEmailSerializer
#     def post(self, request):

#         serializer = self.serializer_class(data=request.data)
#         email = request.data['email']

#         if User.objects.filter(email=email).exists():
#             user = User.objects.get(email=email)
#             uidb64 = urlsafe_base64_encode(smart_bytes(user.id) )
#             token = PasswordResetTokenGenerator().make_token(user)

#             current_site=get_current_site(request=request).domain
#             realtivelink = reverse('password-reset',kwargs={'uidb64':uidb64,'token':token})
                
#             absurl='http://'+current_site+realtivelink
#             email_body='Hi, \nUse link below to reset your password \n' + absurl
#             data={'email_body':email_body,'to_email':user.email,'email_subject':'Reset your password'}
#             Util.send_email(data)
#         return Response({'successfully':'check your email to reset your password'},status=status.HTTP_200_OK)

# class PasswordTokenCheckAPIView(generics.GenericAPIView):
#     def get(self, request, uidb64,token):
#         try:
#             id= smart_str(urlsafe_base64_decode(uidb64))
#             user= User.objects.get(id=id)
#             if not PasswordResetTokenGenerator().check_token(user,token):
#                 return Response({'error':'token is not valid, please check the new one'},status=status.HTTP_401_UNAUTHORIZED)
#             return Response({'sucess':True, 'message':'Credential Valid','uidb64':uidb64, 'token':token},status=status.HTTP_200_OK)


#         except DjangoUnicodeDecodeError as indentifier:
#             return Response({'error':'token is not valid, please check the new one'},status=status.HTTP_401_UNAUTHORIZED)

# class SetNewPasswordAPIView(generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class=ResetPassWordSerializer

#     def patch(self, request):
#         serializer=self.serializer_class(data=request.data)

#         serializer.is_valid(raise_exception=True)

#         return Response({'sucess':True, 'message':'Password is reset successfully'},status=status.HTTP_200_OK)
