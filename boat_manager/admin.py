from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Pier, Boat,Bookings, CustomUser

# Register your models here.
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Pier)
admin.site.register(Boat)
admin.site.register(Bookings)
