from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:car_id>/', views.book_car, name='book_car'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('add_review/<int:car_id>/', views.add_review, name='add_review'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
