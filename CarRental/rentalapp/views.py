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
from django.db.models import Q
from django.contrib import messages
from django.db.models import Count


# Create your views here.
def home(request):
    recommended_cars = []
    if request.user.is_authenticated:
        # Fetch the latest booking of the user
        latest_booking = Booking.objects.filter(user=request.user).order_by('-end_date').first()

        # If there was a booking, fetch other cars of the same type
        if latest_booking:
            car_type = latest_booking.car.type
            recommended_cars = Car.objects.filter(type=car_type, available=True).exclude(id=latest_booking.car.id)[:5]

    context = {
        'recommended_cars': recommended_cars,
    }
    return render(request, 'home.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def book_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.car = car
            booking.user = request.user
            booking.save()

            return redirect('car_detail', car_id=car.id)
        else:
            print(form.errors)  # Add this line

    else:
        form = BookingForm()

    return render(request, 'book_car.html', {'form': form, 'car': car})

def car_catalog(request):
    cars = Car.objects.all()

    # Get search parameters from the query string
    query = request.GET.get('q')
    type_query = request.GET.get('type')

    if query:  # If a query is specified
        # Filter the cars based on the query
        cars = cars.filter(Q(make__icontains=query) | Q(model__icontains=query))

    if type_query:  # If a type is specified
        # Filter the cars based on the type
        cars = cars.filter(type__iexact=type_query)

    return render(request, 'rentalapp/car_catalog.html', {'cars': cars, 'query': query, 'type_query': type_query})

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
            if not Booking.objects.filter(user=request.user, car=car).exists():
                messages.error(request, 'You can only review cars you have rented.')
                return redirect('car_detail', car_id=car.id)
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
