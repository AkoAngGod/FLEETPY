from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Driver, Receipt, Taxi
from .forms import UserRegistrationForm, DriverForm
import random, string
from decimal import Decimal
from django.contrib import messages

def generate_transaction_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

@login_required
def credit_payment(request):

    receipts = Receipt.objects.all().order_by('-time_in')

    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        amount = Decimal(request.POST.get('amount'))
        transaction_number = generate_transaction_number()

        try:
            profile = Profile.objects.get(id=profile_id)
            profile.balance -= amount
            if profile.balance <= 0:
                profile.is_active = False 
            else:
                profile.is_active = True
            profile.save()

            Receipt.objects.create(
                profile=f"{profile.firstname} {profile.lastname}",
                license_number=profile.license_number,
                vehicle="",
                time_in=timezone.now(),
                time_out=timezone.now(),
                rental_days=0,
                total_rent=0,
                payment_amount=amount,
                balance=profile.balance,
                transaction_number=transaction_number
            )

            return redirect('dashboard')
        except Profile.DoesNotExist:
            print("Profile does not exist")

    profiles = Profile.objects.filter(is_active=True)
    return render(request, 'creditpayment.html', {'profiles': profiles, 'receipts': receipts})

@login_required
def edit_profile(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        profile_type = request.POST.get('profile_type')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        date_of_birth = request.POST.get('date_of_birth')
        license_number = request.POST.get('license_number')
        username = request.POST.get('username')

        name_parts = full_name.split(' ')

        if len(name_parts) == 4:
            firstname = name_parts[0] + ' ' + name_parts[1]
            middlename = name_parts[2]
            lastname = name_parts[3]
        elif len(name_parts) == 3:
            firstname = name_parts[0]
            middlename = name_parts[1]
            lastname = name_parts[2]
        elif len(name_parts) == 2:
            firstname = name_parts[0]
            middlename = ''
            lastname = name_parts[1]
        else:
            firstname = full_name
            middlename = ''
            lastname = ''

        profile.role = profile_type
        profile.firstname = firstname
        profile.middlename = middlename
        profile.lastname = lastname
        profile.phone_number = phone_number
        profile.address = address
        profile.date_of_birth = date_of_birth
        profile.license_number = license_number
        
        profile.save() 

        user.email = email
        user.username = username
        user.firstname = firstname
        user.lastname = lastname
        user.save()

        return redirect('dashboard')
    else:
        full_name = f"{profile.firstname} {profile.middlename} {profile.lastname}"
        context = {
            'profile': profile,
            'full_name': full_name,
        }

    return render(request, 'editprofile.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            profile_type = request.POST.get('profile_type')
            user = form.get_user()
            login(request, user)

            if profile_type == 'driver':
                return redirect('driverdashboard')
            elif profile_type == 'admin':
                return redirect('dashboard')
            else:
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    current_user_profile = get_object_or_404(Profile, user=request.user)
    profiles = Profile.objects.all()
    return render(request, 'dashboard.html', {'current_user_profile': current_user_profile,'profiles': profiles})

@login_required
def driverdashboard(request):
    profiles = Profile.objects.all()
    return render(request, 'driverdashboard.html', {'profiles': profiles})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile

def profile_creation(request):
    if request.method == 'POST':
        profile_type = request.POST.get('profile_type')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        date_of_birth = request.POST.get('date_of_birth')
        license_number = request.POST.get('license_number')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        
        if password == confirm_password:
            user = User.objects.create_user(username=username, password=password, email=email)
            Profile.objects.create(
                user=user,
                firstname=full_name.split()[0],
                middlename=' '.join(full_name.split()[1:-1]) if len(full_name.split()) > 2 else '',
                lastname=full_name.split()[-1] if len(full_name.split()) > 1 else '',
                phone_number=phone_number,
                address=address,
                date_of_birth=date_of_birth,
                license_number=license_number,
                role=profile_type,
                photo=request.FILES.get('photo')  
            )
            messages.success(request, f"Account created successfully for {username}!")
            return redirect('register.html')
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
    
    return render(request, 'register.html')

@login_required
def profile_loob(request):
    if request.method == 'POST':
        profile_type = request.POST.get('profile_type')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        date_of_birth = request.POST.get('date_of_birth')
        license_number = request.POST.get('license_number')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if User.objects.filter(username=username).exists():
            return render(request, 'driversprofile.html', {'error': 'Username already exists'})
        
        if password == confirm_password:
            user = User.objects.create_user(username=username, password=password, email=email)
            Profile.objects.create(
                user=user,
                firstname=full_name.split()[0],
                middlename=' '.join(full_name.split()[1:-1]) if len(full_name.split()) > 2 else '',
                lastname=full_name.split()[-1] if len(full_name.split()) > 1 else '',
                phone_number=phone_number,
                address=address,
                date_of_birth=date_of_birth,
                license_number=license_number,
                role=profile_type,
                photo=request.FILES.get('photo')  
            )
            messages.success(request, f"Account created successfully for {username}!")
            return redirect('dashboard')
        else:
            return render(request, 'driversprofile.html', {'error': 'Passwords do not match'})
    
    return render(request, 'driversprofile.html')



@login_required
def billing(request):
    profiles = Profile.objects.all()
    taxis = Taxi.objects.all()
    drivers = Driver.objects.all() 
    receipts = Receipt.objects.all().order_by('-time_in')
    clocked_in_profiles = Driver.objects.filter(time_out__isnull=True).values_list('profile_id', flat=True)

    if request.method == 'POST':
        if 'clock_in' in request.POST:
            profile_id = request.POST.get('profile_id')
            taxi_id = request.POST.get('taxi_id')
            if profile_id and taxi_id:
                try:
                    profile = Profile.objects.get(id=profile_id)
                    taxi = Taxi.objects.get(id=taxi_id)
                    time_in = timezone.now()
                    daily_rate = 1500
                    rental_days = 1
                    payment_amount = 0
                    total_rent = daily_rate * rental_days
                    transaction_number = generate_transaction_number()
                    profile.is_active = True
                    profile.save()

                    Driver.objects.create(
                        profile=profile,
                        license_number=profile.license_number,
                        vehicle=taxi.plate_number,
                        time_in=time_in,
                        rental_days=rental_days,
                        payment_amount=payment_amount,
                        total_rent=total_rent,
                        balance=profile.balance + total_rent,
                        transaction_number=transaction_number
                    )
                    profile.balance += total_rent
                    profile.save()

                    print(f"Clock In: Profile {profile.firstname} {profile.lastname}, Time In: {time_in}, Total Rent: {total_rent}, Transaction Number: {transaction_number}")
                except Profile.DoesNotExist:
                    print("Profile does not exist")
                except Taxi.DoesNotExist:
                    print("Taxi does not exist")
                return redirect('billing')

        elif 'clock_out' in request.POST:
            profile_id = request.POST.get('profile_id')
            if profile_id:
                try:
                    profile = Profile.objects.get(id=profile_id)
                    time_out = timezone.now()

                    driver = Driver.objects.get(profile=profile, time_out__isnull=True)
                    rental_days = (time_out - driver.time_in).days + 1
                    daily_rate = 1500
                    total_rent = rental_days * daily_rate
                    payment_amount = float(request.POST.get('payment_amount'))
                    balance = total_rent - payment_amount
                    if balance <= 0:
                        profile.is_active = False
                        profile.save()
                    else:
                        profile.is_active = True
                        profile.save()
                    receipt = Receipt.objects.create(
                        profile=f"{driver.profile.firstname} {driver.profile.lastname}",
                        license_number=driver.license_number, 
                        vehicle=driver.vehicle,
                        time_in=driver.time_in,
                        time_out=time_out,
                        rental_days=rental_days,
                        total_rent=total_rent,
                        payment_amount=payment_amount,
                        balance=balance,
                        transaction_number=driver.transaction_number
                    )
                    print(f"Receipt created: {receipt.id}")

                    profile.balance = balance
                    print(f"Profile balance updated from {balance} to {profile.balance} for {profile.firstname} {profile.lastname}")

                    driver_id = driver.id
                    driver.delete()
                    driverss = get_object_or_404(driverss, profile=profile)
                    driverss.delete()
                    print(f"Driver entry with ID {driver_id} deleted for Profile {profile.firstname} {profile.lastname}")

                    clocked_in_profiles = Driver.objects.filter(time_out__isnull=True).values_list('profile_id', flat=True)

                except Profile.DoesNotExist:
                    print("Profile does not exist")
                except Driver.DoesNotExist:
                    print("Driver does not exist")
                except Exception as e:
                    print(f"Error during clock out: {e}")
                return redirect('billing')

    return render(request, 'billing.html', {
        'profiles': profiles,
        'taxis': taxis,
        'drivers': drivers, 
        'receipts': receipts,
        'clocked_in_profiles': clocked_in_profiles,
    })

@login_required
def receipt(request, receipt_id):
    try:
        receipt = Receipt.objects.get(id=receipt_id)
        return render(request, 'my_app/receipt_content.html', {'transaction': receipt})
    except Receipt.DoesNotExist:
        return render(request, 'my_app/receipt_content.html', {'error': 'Receipt not found'})

@login_required
def driver_profile(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('billing')
    else:
        form = DriverForm()
    return render(request, 'driversprofile.html', {'form': form})

@login_required
def delete_driver(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    if request.method == "POST":
        driver.delete()
        return redirect('billing') 
    return render(request, 'confirm_delete.html', {'driver': driver})