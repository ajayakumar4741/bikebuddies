from django.shortcuts import render
from rest_framework import generics,permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed,PermissionDenied
from .serializers import *
from .models import *
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly

# Create your views here.

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'bikes': reverse('bike-list', request=request, format=format),
        
    })
    
class BikeList(generics.ListCreateAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    permission_classes = [IsAdminOrReadOnly]
    
class BikeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    permission_classes = [IsAdminOrReadOnly]
    

class BikeImageList(generics.ListCreateAPIView):
    queryset = BikeImage.objects.all()
    serializer_class = BikeImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    
class BikeImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BikeImage.objects.all()
    serializer_class = BikeImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    
class OccupiedDateList(generics.ListCreateAPIView):
    queryset = OccupiedDate.objects.all()
    serializer_class = OccupiedDateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user  
        if not user.is_superuser and not user.is_staff:
            return OccupiedDate.objects.filter(user=user)
        return super().get_queryset()

class OccupiedDateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BikeImage.objects.all()
    serializer_class = OccupiedDateSerializer
    permission_classes = [IsAdminOrReadOnly]
    
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
            raise permissions.PermissionDenied("You do not have permission to access this user's details.")
    
class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def perform_create(self, serializer):
        user = serializer.save()
        token,created=Token.objects.create(user=user)
        
        self.response_data = {
            'user':{
            'id': user.id,
            'username': user.email,
            'email': user.email,
            'full_name': user.full_name,
            },
            'token': token.key
        }
        
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(self.response_data)
        
class Login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            raise AuthenticationFailed('Invalid email or password')
        
        token= Token.objects.get_or_create(user=user)
        
        return Response({
            'user': {
                'id': user.id,
                'username': user.email,
                'email': user.email,
                'full_name': user.full_name,
            },
            'token': token.key
        })