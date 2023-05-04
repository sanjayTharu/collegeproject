from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivateTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk)+str(user.is_active)+str(timestamp)
    
account_activation_token=AccountActivateTokenGenerator()