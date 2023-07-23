from django import forms
from .models import Booking, UserProfile, Review
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class BookingForm(forms.Form):
    pickup_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'], 
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    return_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    comments = forms.CharField(widget=forms.Textarea, required=False)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number']

class EditProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']