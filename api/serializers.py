from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from .models import Movie,Theatre,Show,Seat,Ticket,Payment,Customer


class MovieSerializer(serializers.ModelSerializer):
    recommended_movies = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields='__all__'

    # def get_recommended_movies(self, obj):
    #     # Get the recommended movies for the current movie object
    #     recommended_movies = obj.recommended_movies

       

    #     # Return the serialized recommended movies
    #     return recommended_movies

class TheatreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theatre
        fields='__all__'

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model= Show
        fields='__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields='__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields='__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields='__all__'

class CustomerSerializer(serializers.ModelSerializer):
    confirm_password= serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return super().validate(attrs)
    class Meta:
        model = Customer
        fields = ('email', 'password', 'confirm_password', 'username')


    def create(self,validated_data):
        validated_data.pop('confirm_password',None)
        customer=Customer(email=validated_data['email'],username=validated_data['username'])
        customer.set_password(validated_data['password'])
        return customer
        # #send activation mail
        # current_site=settings.CURRENT_SITE
        # domain=current_site.domain
        # protocol='https' if self.context['request'].is_secure() else 'http'
        # uidb64=urlsafe_base64_encode(force_bytes(customer.pk))
        # token=account_activation_token.make_token(customer)
        # activation_link=reverse('activate',kwargs={'uidb64':uidb64,'token':token})
        # activate_url=f'{protocol}://{domain}{activation_link}'

        # subject='Activate Your Account'
        # message=f'Hi {customer.username},\n\n Please use this link to activate your account:\n\n{activate_url}'
        # from_email=settings.EMAIL_HOST_USER
        # to_email=[customer.email]
        # send_mail(subject,message,from_email,to_email,fail_silently=False)

        # return customer


# class ProfileAdmin(serializers.ModelSerializer):
#     class Meta:
#         model= Profile
#         fields='__all__'


# from rest_framework import serializers

# class ForgotPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField()

# class ResetPasswordSerializer(serializers.Serializer):
#     token = serializers.CharField()
#     password = serializers.CharField(write_only=True)
#     password_confirm = serializers.CharField(write_only=True)

#     def validate(self, data):
#         if data['password'] != data['password_confirm']:
#             raise serializers.ValidationError('Passwords do not match.')
#         return data
# class ForgetPaswordSerializer(serializers.Serializer):
#     class Meta:
#         model=PasswordResetToken
#         fields='__all__'

# from django.contrib.auth.models import User

# class ChangePasswordSerializer(serializers.Serializer):
#     class Meta:
#         model=User
#         old_password=serializers.CharField(required=True)
#         new_password=serializers.CharField(required=True)

