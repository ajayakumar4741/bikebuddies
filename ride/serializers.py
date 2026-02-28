from .models import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


# class BookingSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Booking
#         fields = ['url', 'id', 'user', 'bike', 'start_date', 'end_date',
#                   'status', 'payment_intent_id', 'created_at']

class OccupiedDateSerializer(serializers.HyperlinkedModelSerializer):
    bike = serializers.HyperlinkedRelatedField(
        view_name='bike-detail',
        queryset=Bike.objects.all()
    )
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        queryset=User.objects.all()
    )
    booking = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = OccupiedDate
        fields = ['url','id', 'bike', 'date', 'user', 'booking']
        
class BikeImageSerializer(serializers.ModelSerializer):

    bike = serializers.HyperlinkedRelatedField(
        view_name='bike-detail',
        queryset=Bike.objects.all()
    )
    
    
    class Meta:
        model = BikeImage
        fields = ['id', 'image', 'caption','bike',]

class BikeSerializer(serializers.HyperlinkedModelSerializer):
    occupied_dates = OccupiedDateSerializer(many=True, read_only=True)
    images = BikeImageSerializer(many=True, read_only=True)
    class Meta:
        model = Bike
        fields = ['url', 'id', 'name', 'type', 'pricePerRide', 'currency', 'maxOccupancy', 'description','images','occupied_dates']


        
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username','password','email','full_name']

      # Hash the password before saving     
    def validate_password(self, value):
        return make_password(value)