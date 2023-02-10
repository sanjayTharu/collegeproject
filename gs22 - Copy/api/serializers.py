from rest_framework import serializers
from .models import Movie,Theatre,Show,Seat,Ticket,Payment,Customer,Profile

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields='__all__'

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
    class Meta:
        model = Customer
        fields='__all__'

class ProfileAdmin(serializers.ModelSerializer):
    class Meta:
        model= Profile
        fields='__all__'


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

from django.contrib.auth.models import User

class ChangePasswordSerializer(serializers.Serializer):
    class Meta:
        model=User
        old_password=serializers.CharField(required=True)
        new_password=serializers.CharField(required=True)

