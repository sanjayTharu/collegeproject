from django.db import models
from django.contrib.auth.models import User,AbstractUser
# Create your models here.
#model for Movie
class Movie(models.Model):
    GENRE=(
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

    )

    title=models.CharField(max_length=100)
    release_date=models.DateField()
    genre=models.CharField(max_length=50,choices=GENRE)
    synopsis=models.TextField(max_length=200,blank=True)
    posterurl=models.URLField(blank=True)

    def __str__(self):
        return str(self.title)


#model for Theatre
class Theatre(models.Model):
    THEATRE=(
        ('QFX Cinemas Jalma','QFX Cinemas Jalma'),
        ('Chitwan cineplex','Chitwan cineplex'),
        ('Indradev Cinema','Indredev cinema'),
        ('Ganesh Filmhall','Ganesh Filmhall'),
    )
    name=models.CharField(max_length=100,choices=THEATRE)
    location=models.TextField()
    capacity=models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)


#Model for show
class Show(models.Model):
    START_TIME=(
        ('Morning- 9 AM','Morning- 9 AM'),
        ('Noon- 12 PM','Noon- 12 PM'),
        ('Day- 3 PM','Day- 3 PM'),
        ('Evening- 6 PM','Evening- 6 PM'),
        ('Evening- 9 PM','Evening- 9 PM'),
        ('Night- 12 AM','Night- 12 AM'),
    )
    LANGUAGE=(
        ('Nepali','Nepali'),
        ('Hindi','Hindi'),
        ('English','English'),
        ('Other Regional Language','Other Regional Language'),
    )
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    start_time=models.CharField(choices=START_TIME,max_length=200)
    language=models.CharField(max_length=100,choices=LANGUAGE)

    def __str__(self):
        return str(self.start_time)



#Model for Seat
class Seat(models.Model):
    show=models.ForeignKey(Movie,on_delete=models.CASCADE)
    row=models.PositiveSmallIntegerField()
    number=models.PositiveSmallIntegerField()
    is_available=models.BooleanField(default=True)

    def __str__(self):
        return str(self.number)




#Model for ticket
class Ticket(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    show=models.ForeignKey(Show,on_delete=models.CASCADE)
    show_date=models.DateField()
    seat=models.ForeignKey(Seat,on_delete=models.CASCADE)
    booking_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)



#Model for payment
class Payment(models.Model):
    PAYMENT=(
            ('Esewa','Esewa'),
            ('Khalti','Khalti'),
            ('IMEPay','IMEPay'),
            ('Others','Others'),
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50,choices=PAYMENT)
    transaction_id = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return str(self.id)


class Customer(User):
    phone_number=models.CharField(max_length=10,unique=True)
    address=models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    forget_password_token=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import uuid

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )