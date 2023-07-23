from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    seats = models.IntegerField()
    color = models.CharField(max_length=20)
    price_per_day = models.DecimalField(max_digits=5, decimal_places=2)
    available = models.BooleanField(default=True)
    # new field for the car image
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)

# start
    COUPE_SPORT = 'COUPE/SPORT'
    HATCHBACK = 'HATCHBACK'
    SUV = 'SUV'
    VAN = 'VAN'
    SEDAN = 'SEDAN'

    CAR_TYPE_CHOICES = [
        (COUPE_SPORT, 'Coupe/Sport'),
        (HATCHBACK, 'Hatchback'),
        (SUV, 'SUV/4x4'),
        (VAN, 'Van'),
        (SEDAN, 'Sedan'),
    ]

    type = models.CharField(
        max_length=12,
        choices=CAR_TYPE_CHOICES,
        default=HATCHBACK,
    )
# end

    def __str__(self):
        return f"{self.make} {self.model}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Booking {self.pk} by {self.user.username}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    rental_history = models.ManyToManyField('Booking')
    license_number = models.CharField(max_length=255)

    def get_most_recent_car_type(self):
        # Get the most recent booking made by the user
        recent_booking = self.rental_history.order_by('-end_date').first()

        # Return the type of the car associated with this booking
        if recent_booking:
            return recent_booking.car.type
        else:
            return None

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.IntegerField()
    rating = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(5)
    ])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
