from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .models import Car, Booking, UserProfile, Review
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserProfileForm, BookingForm, ReviewForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Car
from .forms import BookingForm
from django.contrib.auth import logout
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserChangeForm
from .forms import EditProfileForm
from django.shortcuts import render, get_object_or_404
from .models import Car, Review



# Create your views here.
def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def book_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    form = BookingForm(request.POST or None)
    if form.is_valid():
        # You can use form.cleaned_data to access validated form data
        # Save booking to database or perform any other action
        return HttpResponseRedirect('/thanks/')  # Redirect after POST
    return render(request, 'book_car.html', {'car': car, 'form': form})

def car_catalog(request):
    cars = Car.objects.all()
    return render(request, 'rentalapp/car_catalog.html', {'cars': cars})

def car_details(request, car_id):
    car = Car.objects.get(id=car_id)
    return render(request, 'rentalapp/car_details.html', {'car': car})

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('home')
    else:
        user_form = UserCreationForm()
        profile_form = UserProfileForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'registration/profile.html', {'form': form})

@login_required
def add_review(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.car = car
            review.user = request.user
            review.save()
            return redirect('car_detail', car_id=car.id)
    else:
        form = ReviewForm()
    return render(request, 'rentalapp/add_review.html', {'form': form, 'car': car})

@login_required
def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    reviews = Review.objects.filter(car=car)
    
    context = {
        'car': car,
        'reviews': reviews,
        'range': range(0, 5),  # to use in the star display loop
    }
    return render(request, 'rentalapp/car_detail.html', context)
