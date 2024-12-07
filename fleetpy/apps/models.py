from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('driver', 'Driver')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    firstname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255, blank=True)
    lastname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20,default=00000000000)
    address = models.CharField(max_length=255, default='Philippines')
    date_of_birth = models.DateField(default=date.today)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Driver(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)
    vehicle = models.CharField(max_length=100)
    time_in = models.DateTimeField(null=True, blank=True)
    time_out = models.DateTimeField(null=True, blank=True)
    rental_days = models.IntegerField(null=True, blank=True)
    payment_amount = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    total_rent = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    balance = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    transaction_number = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.profile.user.username} - {self.license_number}"

class Receipt(models.Model):
    profile = models.CharField(max_length=255, null=True, blank=True)
    license_number = models.CharField(max_length=50, null=True, blank=True) 
    vehicle = models.CharField(max_length=100, null=True)
    time_in = models.DateTimeField()
    time_out = models.DateTimeField()
    rental_days = models.IntegerField()
    total_rent = models.DecimalField(max_digits=10, decimal_places=2)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Receipt for {self.profile}" if self.profile else f"Receipt (Driver Deleted)"

class Taxi(models.Model):
    plate_number = models.CharField(max_length=7, unique=True)

    def __str__(self):
        return self.plate_number
