from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class Bike(models.Model):
    RIDE_TYPE = [
        ('adventure','adventure'),
        ('street','street'),
        ('long trip','long trip')
    ]
    CURRENCY_TYPES = [
        ('IND','IND'),
        ('USD','USD')
    ]
    name = models.CharField(max_length=255,blank=True,default='')
    type = models.CharField(max_length=244,choices=RIDE_TYPE)
    pricePerRide = models.IntegerField(default=150)
    currency = models.CharField(default="IND", max_length=10, choices=CURRENCY_TYPES)
    maxOccupancy = models.IntegerField(default=1)
    description = models.TextField(max_length=1000)
    
    def __str__(self):
        return f'{self.name} ({self.type})'
    
class BikeImage(models.Model):
    image = models.ImageField(upload_to='room_images/')
    # image = CloudinaryField("image")
    caption = models.CharField(max_length=255, blank=True, null=True)
    bike = models.ForeignKey(Bike, related_name='images', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Image for {self.bike.name} - {self.caption or 'No Caption'}"
    
class OccupiedDate(models.Model):
    bike = models.ForeignKey(Bike, related_name='occupied_dates', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='booked_dates')
    date = models.DateField()
    
    def __str__(self):
        return f"{self.bike.name} occupied on {self.date}"
    
class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100,default='')