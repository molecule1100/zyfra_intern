from django.db import models
from sorl.thumbnail import ImageField


class VehicleType(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    class OperationStatusChoices(models.TextChoices):
        IN_USE = 'В работе'
        IDLE = 'Простой'
        REPAIR = 'Ремонт'

    reg_number = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    date_purchase = models.DateField()
    type = models.ForeignKey(VehicleType, on_delete=models.SET_NULL, null=True)
    mileage = models.DecimalField(max_digits=7, decimal_places=0)
    operation_status = models.CharField(max_length=50, choices=OperationStatusChoices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class VehicleImage(models.Model):
    file = ImageField(upload_to='vehicle/images/')
    vehicle = models.ForeignKey(Vehicle, related_name='images', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
