from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.contrib.auth import get_user_model
import pandas as pd
from sklearn.neighbors import DistanceMetric, NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from django.utils.translation import gettext_lazy as _
from .manager import UserManager
import csv


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
    poster=models.ImageField(upload_to='movie_images/')
    recommended_movies = models.JSONField(default=list)
    
    def __str__(self):
        return str(self.title)

    def update_recommended_movies(self):
        # load movies.csv and ratings.csv files
        movies_df = pd.read_csv('data/movies.csv')
        ratings_df = pd.read_csv('data/ratings.csv')

        # merge the two dataframes using movieId column as key
        df = pd.merge(movies_df, ratings_df, on='movieId')

        # pivot the merged dataframe to create user-movie rating matrix
        matrix_df = df.pivot_table(index='userId', columns='title', values='rating')

        # fill missing values with 0
        matrix_df.fillna(0, inplace=True)

        # compute pairwise similarity matrix
        similarity_matrix = cosine_similarity(matrix_df)

        # implement K-Nearest Neighbors algorithm to find most similar movies
        knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10)
        knn.fit(similarity_matrix)
        movie_title = self.title.lower()
        movie_index = matrix_df.columns.get_loc(movie_title)
        distances, indices = knn.kneighbors(matrix_df.iloc[:, movie_index].values.reshape(1, -1))

        # update recommended_movies field
        recommended_movies = []
        for i in range(1, len(distances.flatten())):
            recommended_movies.append(matrix_df.columns[indices.flatten()[i]])
        self.recommended_movies.set(recommended_movies)

    def save(self, *args, **kwargs):
        # update recommended movies before saving
        self.update_recommended_movies()
        super().save(*args, **kwargs)
    




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




class Customer(AbstractBaseUser):
    email=models.EmailField(unique=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)

    
    
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS=[]

    objects=UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


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

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50,choices=(
            ('Esewa','Esewa'),
            ('Khalti','Khalti'),
            ('Others','Others'),
    ),default='khalti')
    is_verified=models.BooleanField(default=False)
    is_paid=models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=20,null=True)
    payment_date = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f"Payment {self.customer} -{self.amount}"
    


    


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