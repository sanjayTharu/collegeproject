from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.
#model for Movie
class Movie(models.Model):
    
    

    title=models.CharField(max_length=100)
    release_date=models.DateField()
    genre=models.CharField(max_length=50,choices=(
        ('Action','Action'),
        ('Comedy','Comedy'),
        ('Horror','Horror'),
        ('Documentary','Dcoumentary'),
        ('Science Fiction','Science Fiction'),
        ('Romantic','Romantic'),
        ('Drama','Drama'),
        ('Western','Western'),
        ('Thriller','Thriller'),
        ('Animation','Animation'),
        ('Adventure','Adventure'),
        ('Romantic comedy','Romantic Comedy'),
        ('Crime Film','Crime Film'),
        ('Fantasy','Fantasy'),
        ('Film Noir','Film Noir'),
        ('War','War'),
        ('Experimental','Experimental'),
        ('Mystery','Mystery'),
        ('Biographical','Biographichal'),
        ('Dark Comedy','Dark Comedy'),
        ('Historical Film','Historical Film'),
        ('Short','Short'),
        ('Spy','Spy'),
        ('Musical','Musical'),

    ),default='ACTION')
    description=models.TextField(max_length=200,blank=True)
    posterurl=models.URLField(blank=True)

    def __str__(self):
        return str(self.title)


#model for Theatre
class Theatre(models.Model):
    name=models.CharField(max_length=100,choices=(
        ('QFX Cinemas Jalma','QFX Cinemas Jalma'),
        ('Chitwan cineplex','Chitwan cineplex'),
        ('Indradev Cinema','Indredev cinema'),
        ('Ganesh Filmhall','Ganesh Filmhall'),
    ),default='QFX Cinemas Jalma')
    location=models.TextField()

    def __str__(self):
        return str(self.name)


#Model for show
class Show(models.Model):

    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    theater=models.ForeignKey(Theatre,on_delete=models.CASCADE)
    start_time=models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title} at {self.theater.name}"



#Model for Seat
class Seat(models.Model):
    theater=models.ForeignKey(Theatre,on_delete=models.CASCADE)
    row_number= models.PositiveIntegerField()
    seat_number=models.PositiveIntegerField()
    is_booked=models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.row_number}-{self.seat_number} at {self.theater.name}"
    
    class Meta:
        unique_together=['theater','row_number','seat_number']




class CustomManager(BaseUserManager):
    def create_user(self, email,password=None,**extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(email,password,**extra_fields)



class Customer(AbstractBaseUser):
    email=models.EmailField(unique=True)
    first_name=models.CharField(max_length=150)
    last_name=models.CharField(max_length=150)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    objects=CustomManager()
    
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS=['first_name','last_name']

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_staff
    def has_module_perms(self,app_label):
        return self.is_staff




#Model for ticket
class Ticket(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    show=models.ForeignKey(Show,on_delete=models.CASCADE)
    show_date=models.DateField()
    seat=models.ForeignKey(Seat,on_delete=models.CASCADE)
    booking_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.id}"



#Model for payment
class Payment(models.Model):

    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50,choices=(
            ('Esewa','Esewa'),
            ('Khalti','Khalti'),
            ('IMEPay','IMEPay'),
            ('Others','Others'),
    ),default='')
    transaction_id = models.CharField(max_length=100,null=True)
    payment_date = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f"Payment {self.id}"
    


# class Profile(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     forget_password_token=models.CharField(max_length=100)
#     created_at=models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.username
    
# from django.contrib.auth.models import User
# from django.db import models
# from django.utils import timezone
# import uuid

# class PasswordResetToken(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     token = models.UUIDField(default=uuid.uuid4)
#     created_at = models.DateTimeField(default=timezone.now)
#     is_used = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.username


# from django.dispatch import receiver
# from django.urls import reverse
# from django_rest_passwordreset.signals import reset_password_token_created
# from django.core.mail import send_mail  


# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

#     email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

#     send_mail(
#         # title:
#         "Password Reset for {title}".format(title="Some website title"),
#         # message:
#         email_plaintext_message,
#         # from:
#         "noreply@somehost.local",
#         # to:
#         [reset_password_token.user.email]
#     )