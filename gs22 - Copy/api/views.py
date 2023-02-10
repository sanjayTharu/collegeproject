from django.shortcuts import render
from .serializers import MovieSerializer,TheatreSerializer,ShowSerializer,SeatSerializer,TicketSerializer,PaymentSerializer,CustomerSerializer
from .models import Movie,Theatre,Show,Seat,Ticket,Payment,Customer
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
# Create your views here.

class MovieVIewSet(viewsets.ModelViewSet):
    serializer_class=MovieSerializer
    queryset=Movie.objects.all()
    permission_classes=[IsAuthenticatedOrReadOnly]

class TheatreViewSet(viewsets.ModelViewSet):
    serializer_class=TheatreSerializer
    queryset=Theatre.objects.all()

class ShowViewSet(viewsets.ModelViewSet):
    serializer_class=ShowSerializer
    queryset=Show.objects.all()

class SeatViewSet(viewsets.ModelViewSet):
    serializer_class=SeatSerializer
    queryset=Seat.objects.all()

class TIcketViewSet(viewsets.ModelViewSet):
    serializer_class=TicketSerializer
    queryset=Ticket.objects.all()

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class=PaymentSerializer
    queryset=Payment.objects.all()

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class=CustomerSerializer
    queryset=Customer.objects.all()


from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated

class ChangepasswordView(generics.UpdateAPIView):
    
    serializer_class=ChangePasswordSerializer
    model=User
    permission_classes=[IsAuthenticated]

    def get_object(self,queryset=None):
        obj=self.request.user
        return obj

    def update(self,request,*args,**kwargs):
        self.object=self.get_object()
        serializer=self.get_serializer(data=request.data)

        if serializer.is_valid():
            # check old Password
            if not self.object.check_password(serializer.data.get("old password")):
                return Response({"old password":["wrong password"]},status=status.HTTP_400_BAD_REQUEST)
            #set password also hashes tha password that user will get
            self.object.set_password(serializer.data.get("new password"))
            self.object.save()
            response={
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail, send_mass_mail

class SendFormEmail(View):

    def  get(self, request):

        # Get the form data 
        name = request.GET.get('name', None)
        email = request.GET.get('email', None)
        message = request.GET.get('message', None)

        # Send Email
        send_mail(
            'Subject - Django Email Testing', 
            'Hello ' + name + ',\n' + message, 
            'sender@example.com', # Admin
            [
                email,
            ]
        ) 

        # Redirect to same page after form submit
        messages.success(request, ('Email sent successfully.'))
        return redirect('home') 

        send_mail(
            'subject', 
            'body of the message', 
            'sender@example.com', 
            [
                'receiver1@example.com', 
                'receiver2@example.com'
            ]
        ) 
        message1 = ('Subject here', 'Here is the message', 'from@example.com', ['first@example.com', 'other@example.com'])
        message2 = ('Another Subject', 'Here is another message', 'from@example.com', ['second@test.com'])

        send_mass_mail((message1, message2), fail_silently=False)
# from rest_framework import generics, permissions
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
