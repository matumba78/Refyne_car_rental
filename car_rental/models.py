from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    """
        Users within the Django authentication system are represented by this
        model.
    """
    contact_number =  models.CharField(max_length=30, unique=True)


class Car(models.Model):
    carLicenseNumber = models.CharField(max_length=30, primary_key=True)
    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    base_price = models.FloatField()
    pph = models.FloatField()
    security_deposit = models.FloatField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.carLicenseNumber

    @staticmethod
    def get_car_pricing(start_date, end_date, car_id):
        delta = ((end_date - start_date).seconds)/3600
        try:
            car = Car.objects.get(pk=car_id)
        except Car.DoesNotExist:
            return False, None, "Car Does not Exist"
        pricing = delta * car.pph
        return True, pricing, car


class SlotBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    car = models.ForeignKey(Car, on_delete=models.PROTECT)
    toDate = models.DateTimeField()
    fromDate = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)



