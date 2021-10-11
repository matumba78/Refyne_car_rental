from django.urls import path
from car_rental.views import *

urlpatterns = [
    path('create_user/', UserCreateAPIView.as_view(), name="users"),
    path('users/', UserProfileChangeAPIView.as_view(), name="update_users"),
    path('car/', CarHandlerView.as_view(), name="cars"),
    path('search-cars/', CarAvailaibility.as_view(), name="search-cars"),
    path('calculate-price/', CarPricing.as_view(), name="calculate-price"),
    path('user/bookings/', UserBookings.as_view(), name="user-booking"),
    path('car/bookings/', CarUserBookingView.as_view(), name="car-booking"),
    path('car/book/', CarBooking.as_view(), name="book-cars"),

]