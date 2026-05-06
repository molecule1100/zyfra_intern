from django.db import models
from sorl.thumbnail import ImageField
from vehicle.models import Vehicle


class SparePartType(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SparePart(models.Model):
    class StatusChoices(models.TextChoices):
        IN_USE = '1', 'Установлено'
        IN_STOCK = '2', 'На складе'
        REPAIR = '3', 'Ремонт'
        WAITING_REPAIR = '4', 'Ожидает ремонт'

    spare_part_type = models.ForeignKey(SparePartType, on_delete=models.SET_NULL, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, choices=StatusChoices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        vehicle_str = str(self.vehicle) if self.vehicle else "без техники"
        type_str = self.spare_part_type.name if self.spare_part_type else "без типа"
        return f"{type_str} ({vehicle_str})"


class SparePartImage(models.Model):
    file = ImageField(upload_to='images/')
    vehicle = models.ForeignKey(SparePart, related_name='images', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class Attribute(models.Model):
    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    data_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    spare_part_type = models.ForeignKey(SparePartType, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
