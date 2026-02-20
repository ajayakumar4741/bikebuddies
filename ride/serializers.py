from .models import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class OccupiedDateSerializer(serializers.HyperlinkedModelSerializer):
    bike = serializers.HyperlinkedRelatedField(
        view_name='bike-detail',
        queryset=Bike.objects.all()
    )
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        queryset=User.objects.all()
    )
    
    class Meta:
        model = OccupiedDate
        fields = ['url','id', 'bike', 'date', 'user']
        
class BikeImageSerializer(serializers.ModelSerializer):

    bike = serializers.HyperlinkedRelatedField(
        view_name='bike-detail',
        queryset=Bike.objects.all()
    )
    # image = serializers.SerializerMethodField()

    # def get_image(self, obj):
    #     return obj.image.url  # Ensures the full URL is returned

    
    class Meta:
        model = BikeImage
        fields = ['id', 'image', 'caption','bike',]

class BikeSerializer(serializers.HyperlinkedModelSerializer):
    occupied_dates = OccupiedDateSerializer(many=True, read_only=True)
    images = BikeImageSerializer(many=True, read_only=True)
    class Meta:
        model = Bike
        fields = ['url', 'id', 'name', 'type', 'pricePerRide', 'currency', 'maxOccupancy', 'description','images','occupied_dates']
        


# class BikeImageSerializer(serializers.ModelSerializer):
#     bike = serializers.HyperlinkedRelatedField(
#         view_name='bike-detail',
#         queryset=Bike.objects.all()
#     )
#     image = serializers.SerializerMethodField()

#     def get_image(self, obj):
#         request = self.context.get('request')
#         if obj.image and hasattr(obj.image, 'url'):
#             return request.build_absolute_uri(obj.image.url)
#         return None

#     class Meta:
#         model = BikeImage
#         fields = ['id', 'image', 'caption', 'bike']


        
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username','password','email','full_name']

      # Hash the password before saving     
    def validate_password(self, value):
        return make_password(value)