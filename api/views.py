from django.shortcuts import render
from .serializers import MovieSerializer,TheatreSerializer,ShowSerializer,SeatSerializer,TicketSerializer,PaymentSerializer,CustomerSerializer
from .models import Movie,Theatre,Show,Seat,Ticket,Payment,Customer
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate,get_user_model,logout,login
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User,update_last_login
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated,AllowAny
from django.contrib.auth.tokens import default_token_generator
import pickle
from rest_framework.parsers import JSONParser
from django.contrib.auth import get_user_model
User=get_user_model()
  

class CustomPagination(PageNumberPagination):
    page_size=10
    page_query_param='page_size'
    max_page_size=100


class MovieVIewSet(viewsets.ModelViewSet):
    
    queryset=Movie.objects.all()
    serializer_class=MovieSerializer

    permission_classes=[IsAuthenticatedOrReadOnly]
    pagination_class=CustomPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        recommended_movies = instance.recommended_movies.all()
        recommended_serializer = self.get_serializer(recommended_movies, many=True)
        response_data = {
            'movie': serializer.data,
            'recommended_movies': recommended_serializer.data
        }
        return Response(response_data)

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

    @action(detail=True, methods=['post'])
    def verify_payment(self, request, pk=None):
        payment = self.get_object()
        if payment.payment_gateway == 'khalti':
            url = "https://khalti.com/api/v2/payment/verify/"
            payload = {
                'token': payment.transaction_id,
                'amount': payment.amount
            }
            headers = {
                'Authorization': 'Key test_secret_key_f59e8b7d18b4499ca40f68195a846e9b'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            response_data = response.json()
            if response_data.get('state') == 'Completed':
                payment.is_paid = True
                payment.save()
                return Response({'message': 'Payment verification successful'})
            else:
                return Response({'error': 'Payment verification failed'})
        elif payment.payment_gateway == 'esewa':
            url = "https://uat.esewa.com.np/epay/transrec"
            data = {
                'amt': payment.amount,
                'scd': payment.scd,
                'rid': payment.rid,
                'pid': payment.pid,
            }
            response = requests.post(url, data)
            response_data = response.json()
            if response_data.get('success') == 'yes' and response_data.get('amount') == payment.amount:
                payment.is_paid = True
                payment.save()
                return Response({'message': 'Payment verification successful'})
            else:
                return Response({'error': 'Payment verification failed'})
        else:
            return Response({'error': 'Invalid payment gateway'})


    
    

## This is the Customer viewset using jwt authentication
class CustomerViewSet(viewsets.ModelViewSet):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    permission_classes=[AllowAny]
    parser_classes = [JSONParser]

    def create(self,request,*args,**kwargs):
        username=request.data.get('username')
        email=request.data.get('email')
        password=request.data.get('password')
        confirm_password=request.data.get('confirmpass')


        if password != confirm_password:
            return Response({'error':'Password and confirm passwpord didnot match'},status=status.HTTP_400_BAD_REQUEST)
        
        # create the user
        User = get_user_model()

        user=User.objects.create_user(username=username,email=email,password=password)
        serializer=self.get_serializer(user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def login(self,request,*args,**kwargs):
        email=request.data.get('email')
        password=request.data.get('password')
        user=authenticate(request,email=email,password=password)

        if user:
            return Response({'message':'Login Successful'},status=status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid Username and Password'},status=status.HTTP_400_BAD_REQUEST)
        



    # permission_classes_by_action={
    #     'create':[AllowAny],
    #     'login':[AllowAny],
    #     'change_password':[IsAuthenticated]
    #     }
    # pagination_class=CustomPagination

    ## defining permission classes
    # def get_permissions(self):
    #     try:
    #         return [permission() for permission in self.permission_classes_by_action[self.action]]
    #     except KeyError as e:

    #         return [permission() for permission in self.permission_classes]




    # This code is for creating new user or custoner with email and password entered by user

    # def create(self,request,*args,**kwargs):
    #     action = request.data.get('action')
    #     if action == 'register':
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

    #     elif action == 'login':
    #         email = request.data.get('email')
    #         password = request.data.get('password')

    #         user = authenticate(request, username=email, password=password)

    #         if user:
    #             login(request, user)
    #             return Response({'message': 'Login successful'},status=status.HTTP_200_OK)
    #         else:
    #             return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
            
    #     elif action == 'change_password':
    #         user = request.user
    #         current_password = request.data.get('current_password')
    #         new_password = request.data.get('new_password')

    #         if not user.check_password(current_password):
    #             return Response({'error': 'Invalid current password'}, status=status.HTTP_400_BAD_REQUEST)

    #         user.password = make_password(new_password)
    #         user.save()
    #         return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

    #     else:
    #         return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)


    # def get_queryset(self):
    #     return self.queryset.filter(is_superuser=False)

    # def perform_create(self, serializer):
    #     if 'password' in self.request.data:
    #         password = self.request.data['password']
    #         full_name = self.request.data['full_name']
    #         serializer.save(password=password, full_name=full_name)
    #     else:
    #         serializer.save()

    # def perform_update(self, serializer):
    #     if 'password' in self.request.data:
    #         password = self.request.data['password']
    #         serializer.save(password=password)
    #     else:
    #         serializer.save()
        # email=request.data.get('email')
        # password=request.data.get('password')

        # user=authenticate(request,email=email,password=password)

        # if user:
        #     refresh=RefreshToken.for_user(user)
        #     serializer=self.get_serializer(user)
        #     return Response({'token':str(refresh.access_token),'user':serializer.data},status=status.HTTP_200_OK)
        # else:
        #     return Response({'error':'Invalid email or password'},status=status.HTTP_401_UNAUTHORIZED)
        

    ## This code is for updating password while user is logged in

    # def update(self,request,*args,**kwargs):
    #     instance=self.get_object()
    #     current_password=request.data.get('current_password')
    #     new_pasword=request.data.get('new_password')

    #     if not instance.check_password(current_password):
    #         return Response({'error':'Invalid current password'},status=status.HTTP_400_BAD_REQUEST)
        

    #     instance.set_password(new_pasword)
    #     instance.save()
    #     update_last_login(None,instance)
    #     return Response({'message':'Password updated successfully'},status=status.HTTP_200_OK)
    
    # ## this code is used for forget password

class ForgotPasswordViewSet(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        email = request.data.get('email')
        try:
            User = get_user_model()

            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        token = default_token_generator.make_token(user)
        reset_link = f"{settings.FRONTEND_URL}/reset-password/?token={token}"
        message = f"Hi {user.username},\n\nPlease click the link below to reset your password:\n{reset_link}"
        send_mail('Reset Password', message, settings.EMAIL_HOST_USER, [email])
        return Response({'message': 'Reset password link has been sent to your email'}, status=status.HTTP_200_OK)

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
