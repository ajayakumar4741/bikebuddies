from django.urls import path
from . import views
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('bikes/', views.BikeList.as_view(), name='bike-list'),
    path('bikes/<int:pk>/', views.BikeDetail.as_view(), name='bike-detail'),    
    path('bikeimages/', views.BikeImageList.as_view(), name='bikeimage-list'),
    path('bikeimages/<int:pk>', views.BikeImageDetail.as_view(), name='bikeimage-detail'),
    path('occupied-dates/',views.OccupiedDateList.as_view(),name='occupieddate-list'),
    path('occupied-dates/<int:pk>/',views.OccupiedDateDetail.as_view(),name='occupieddate-detail'),
    path('users/',views.UserList.as_view(),name='user-list'),
    path('users/<int:pk>/',views.UserDetail.as_view(),name='user-detail'),
    path('login/', views.Login.as_view(), name='login'),
    path('register/',views.Register.as_view(),name='register'),
    path("bookings/<int:booking_id>/cancel/", cancel_booking, name="cancel-booking"),

    path('create-payment-intent/', views.CreatePaymentIntentView.as_view(), name='create-payment-intent'),
] 

urlpatterns = format_suffix_patterns(urlpatterns)

