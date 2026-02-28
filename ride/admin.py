from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Bike)
admin.site.register(BikeImage)
admin.site.register(OccupiedDate)
admin.site.register(User)
# admin.site.register(Booking)