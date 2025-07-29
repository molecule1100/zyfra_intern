from django.db import models
from vehicle.models import Vehicle
from sorl.thumbnail import ImageField


class SparePartType(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SparePart(models.Model):
    class Status(models.TextChoices):
        INSTALLED = 'Установлено'
        IN_STOCK = 'На складе'
        REPAIR = 'В ремонте'
        AWAITING_REPAIR = 'Ожидает ремонт'

    spare_part_type = models.ForeignKey(SparePartType, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=Status.choices)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)


class SparePartImage(models.Model):
    file = ImageField(upload_to='frontend/spare_parts/images/', blank=True, null=True)
    vehicle = models.ForeignKey(SparePart, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)


class Attribute(models.Model):
    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    data_type = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    spare_part_type = models.ForeignKey(SparePartType, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)
