from django.db import models
from sorl.thumbnail import ImageField


class VehicleType(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    class OperationStatus(models.TextChoices):
        IN_USE = 'in_use', 'В работе'
        IDLE = 'idle', 'Простой'
        REPAIR = 'repair', 'Ремонт'

    reg_number = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    date_purchase = models.DateField()
    type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    mileage = models.DecimalField(max_digits=10, decimal_places=0)
    operation_status = models.CharField(max_length=50, choices=OperationStatus.choices)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.brand


class VehicleImage(models.Model):
    file = ImageField(upload_to='vehicle/images/', blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)
