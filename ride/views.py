from django.shortcuts import render
from rest_framework import generics,permissions,status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed,PermissionDenied
from .serializers import *
from .models import *
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
import stripe
from django.conf import settings
import datetime

# later we reference BookingSerializer explicitly if needed

stripe.api_key = settings.STRIPE_SECRET_KEY



class CreatePaymentIntentView(APIView):
    def post(self, request):
        amount = request.data.get('amount')
        currency = request.data.get('currency')
        email = request.data.get("user_email")
        if not email:
            return Response({'error': 'Invalid email'}, status=400)
        if not amount or int(amount) <= 0:
            return Response({'error': 'Invalid amount'}, status=400)
        if not currency:
            return Response({'error': 'Currency is required'}, status=400)
        
        supported_currencies = ['usd', 'eur', 'inr']
        if currency.lower() not in supported_currencies:
            return Response({'error': 'Unsupported currency'}, status=400)

        try:
            # Create the Stripe payment intent
            intent = stripe.PaymentIntent.create(
                amount=int(amount),  # Amount in cents
                currency=currency,
            )
            
            # Save to the database
            payment_data = {
                'amount': amount,
                'currency': currency,
                'stripe_payment_id': intent['id'],
                'user_email':email
            }
            serializer = PaymentSerializer(data=payment_data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'clientSecret': intent['client_secret'],
                    'payment': serializer.data,
                    
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=400)

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
    queryset = OccupiedDate.objects.all()
    serializer_class = OccupiedDateSerializer
    permission_classes = [IsAdminOrReadOnly]
    
 


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_range(request):
    start_date = request.data.get("start_date")
    end_date = request.data.get("end_date")

    try:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return Response({"error": "Invalid date format, use YYYY-MM-DD"}, status=400)

    qs = OccupiedDate.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=end_date
    )
    count = qs.count()
    print(count)
    qs.delete()
    return Response({"message": f"Cancelled {count} occupied dates"}, status=200)

   
    


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_all(request):
    qs = OccupiedDate.objects.filter(user=request.user)
    count = qs.count()
    qs.delete()
    return Response({"message": f"Cancelled {count} occupied dates"}, status=200)



    
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
        token = Token.objects.create(user=user)
        
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
        
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': {
                'id': user.id,
                'username': user.email,
                'email': user.email,
                'full_name': user.full_name,
            },
            'token': token.key
        })


