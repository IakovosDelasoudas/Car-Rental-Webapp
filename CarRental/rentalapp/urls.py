from django.urls import path
from .views import logout_view, profile
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('car_catalog/', views.car_catalog, name='car_catalog'),
    path('book/<int:car_id>/', views.book_car, name='book_car'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('add_review/<int:car_id>/', views.add_review, name='add_review'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('car_detail/<int:car_id>/', views.car_detail, name='car_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)