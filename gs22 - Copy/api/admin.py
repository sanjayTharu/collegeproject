from django.contrib import admin
from .models import Movie,Theatre,Show,Seat,Ticket,Payment,Customer,Profile
# Register your models here.

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display=['id','title','release_date','genre','synopsis','posterurl']


@admin.register(Theatre)
class TheatreAdmin(admin.ModelAdmin):
    list_display=['id','name','location','capacity']


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display=['id','movie','start_time','language']

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display=['id','show','row','number','is_available']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display=['id','user','show','show_date','seat','booking_date']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=['id','user','ticket','amount','payment_method','transaction_id','payment_date']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['id','username','email','address','password']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['id','user','forget_password_token','created_at']