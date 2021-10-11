from rest_framework import serializers
from car_rental.models import User, Car, SlotBooking


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'contact_number', 'password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'contact_number', 'password')


class UserSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'contact_number')


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = "__all__"


class SlotBookingSerializer(serializers.ModelSerializer):
    car = CarSerializer()
    price = serializers.SerializerMethodField()

    class Meta:
        model = SlotBooking
        fields = ["car", "price", "toDate", "fromDate"]

    def get_price(self, obj):
        status, price, data = Car.get_car_pricing(obj.fromDate, obj.toDate, obj.car_id)
        if status:
            return price
        return "price not available"


class SlotBookingUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = SlotBooking
        fields = ["user", "toDate", "fromDate"]

    def get_user(self, obj):
        return UserSmallSerializer(obj.user).data if obj.user else None




