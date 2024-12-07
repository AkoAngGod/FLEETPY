from django.contrib import admin
from .models import Profile, Driver, Receipt, Taxi

# Register your models here.
admin.site.register(Profile)
admin.site.register(Driver)
admin.site.register(Receipt)
admin.site.register(Taxi)
