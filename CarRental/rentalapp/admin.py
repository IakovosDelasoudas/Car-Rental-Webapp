from django.contrib import admin
from .models import Car, Booking, Review, UserProfile

class CarAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'price_per_day']

class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'start_date', 'end_date']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'rating', 'created_at']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'license_number']

admin.site.register(Car, CarAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
