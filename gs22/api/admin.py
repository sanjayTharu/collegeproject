from django.contrib import admin
from .models import Movie,Theatre,Show,Seat,Ticket,Payment,Customer
# Register your models here.

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display=['id','title','release_date','genre','description','posterurl']


@admin.register(Theatre)
class TheatreAdmin(admin.ModelAdmin):
    list_display=['id','name','location']


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display=['id','movie','theater','start_time']

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display=['id','theater','row_number','seat_number','is_booked']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display=['id','customer','show','show_date','seat','booking_date']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=['id','customer','ticket','amount','payment_method','transaction_id','payment_date']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['id','email','first_name','last_name','is_active','is_staff']

# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display=['id','user','forget_password_token','created_at']