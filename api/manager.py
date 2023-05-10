from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email,password=None,**extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        
        
        user=self.model(email=self.normalize_email(email),
                        **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
       
        extra_fields.setdefault('is_staff',True)
        
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_admin', True)

        return self.create_user(email,password,**extra_fields)
    
    def get_by_natural_key(self, email):
        return self.get(email=email)

    def get_or_create(self, email, **kwargs):
        defaults = kwargs.setdefault('defaults', {})
        defaults['email'] = email
        return super().get_or_create(**kwargs)

    def normalize_email(self, email):
        return super().normalize_email(email)



