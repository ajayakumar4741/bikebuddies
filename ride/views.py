from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from .serializers import *
from .models import *
from rest_framework.reverse import reverse
# Create your views here.

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'bikes': reverse('bike-list', request=request, format=format),
        
    })
    
class BikeList(generics.ListCreateAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    permission_classes = [IsAdminUser]
    
class BikeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    
    
# views.py
class BikeImageList(generics.ListCreateAPIView):
    queryset = BikeImage.objects.all()
    serializer_class = BikeImageSerializer
    permission_classes = [IsAdminUser]

class BikeImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BikeImage.objects.all()
    serializer_class = BikeImageSerializer
    permission_classes = [IsAdminUser]
    
class OccupiedDateList(generics.ListCreateAPIView):
    queryset = OccupiedDate.objects.all()
    serializer_class = OccupiedDateSerializer
    
    def get_queryset(self):
        user = self.request.user  
        if not user.is_superuser and not user.is_staff:
            return OccupiedDate.objects.filter(user=user)
        return super().get_queryset()

class OccupiedDateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BikeImage.objects.all()
    serializer_class = OccupiedDateSerializer
    
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(id=user.id)
        
class UserDetail(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_object(self):
        user = self.request.user
        obj = super().get_object()
        if obj == user or user.is_staff or user.is_superuser:
            return obj
        else:
            return user
    