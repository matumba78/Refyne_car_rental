from rest_framework import generics, mixins, permissions
from rest_framework.permissions import AllowAny
from .models import User, Car, SlotBooking
from .serializers import UserSerializer, CarSerializer, SlotBookingSerializer, SlotBookingUserSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from dateutil import parser


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id


class UserProfileChangeAPIView(generics.RetrieveAPIView,
                               mixins.DestroyModelMixin,
                               mixins.UpdateModelMixin):
    permission_classes = (
        permissions.IsAuthenticated,
        UserIsOwnerOrReadOnly,
    )
    serializer_class = UserSerializer

    def get_object(self):
        username = self.request.user.username
        obj = get_object_or_404(User, username=username)
        return obj

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CarHandlerView(generics.ListCreateAPIView,
                     mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CarAvailaibility(APIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        to_date_time = request.query_params.get('toDateTime', None)
        from_date_time = request.query_params.get('fromDateTime', None)
        to_date_time = parser.parse(to_date_time)
        from_date_time = parser.parse(from_date_time)
        if not to_date_time or not from_date_time:
            return Response("Date range is required to search cars availability")
        query = SlotBooking.objects.filter(fromDate__gte=from_date_time,
                                           toDate__lte=to_date_time).values_list('car_id')
        car_objects = Car.objects.exclude(pk__in=query)
        if not car_objects:
            return Response("No cars available")
        return Response(CarSerializer(car_objects, many=True).data, status=200)


class CarPricing(APIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        to_date_time = request.query_params.get('toDateTime', None)
        from_date_time = request.query_params.get('fromDateTime', None)
        car_id = request.query_params.get('car_id', None)
        if not to_date_time or not from_date_time or not car_id:
            return Response("[ Date range / car ID ] is required to find car pricing")
        to_date_time = parser.parse(to_date_time)
        from_date_time = parser.parse(from_date_time)
        status, price, data = Car.get_car_pricing(from_date_time, to_date_time, car_id)
        if not status:
            return Response({
                "error": "price not found",
                "message": data
            })
        return Response({
            "car_id": data.id,
            "pph": data.pph,
            "price": price
        })


class UserBookings(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = SlotBookingSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        return SlotBooking.objects.filter(user=self.request.user)


class CarUserBookingView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = SlotBookingUserSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        car_id = self.kwargs['car_id']
        return SlotBooking.objects.filter(car_id=int(car_id))


class CarBooking(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        car_id = request.data.get("car_id")
        to_date_time = request.query_params.get('toDateTime', None)
        from_date_time = request.query_params.get('fromDateTime', None)
        try:
            Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response("This car does not exist", status=400)
        availability = SlotBooking.objects.filter(car_id=car_id, toDate__lte=to_date_time, fromDate__gte=from_date_time)
        if availability:
            return Response("Car not available for this time range")
        data = SlotBooking.objects.create(car_id=car_id,
                                        user=request.user,
                                        toDate=to_date_time,
                                        fromDate=from_date_time)
        return Response(CarSerializer(data).data, status=201)














