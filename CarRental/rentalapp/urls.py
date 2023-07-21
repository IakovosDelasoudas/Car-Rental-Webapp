from django.urls import path
from . import views

urlpatterns = [
    path('cars/', views.car_catalog, name='car_catalog'),
    path('cars/<int:car_id>/', views.car_details, name='car_details'),
]
