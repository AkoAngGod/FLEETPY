from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Driver, Profile

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'firstname', 'middlename', 'lastname', 'phone_number', 'address', 'date_of_birth', 'license_number', 'photo']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already in use.")
        return email

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['profile', 'license_number', 'vehicle', 'time_in', 'time_out', 'rental_days', 'payment_amount', 'total_rent', 'balance', 'transaction_number']
