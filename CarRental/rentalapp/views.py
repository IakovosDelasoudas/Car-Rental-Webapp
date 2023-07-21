from django.shortcuts import render
from .models import Car

# Create your views here.
def car_catalog(request):
    cars = Car.objects.all()
    return render(request, 'rentalapp/car_catalog.html', {'cars': cars})

def car_details(request, car_id):
    car = Car.objects.get(id=car_id)
    return render(request, 'rentalapp/car_details.html', {'car': car})
