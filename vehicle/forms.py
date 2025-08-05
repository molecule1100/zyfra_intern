from django import forms
from .models import VehicleType, Vehicle


class CreateUpdateVehicleTypeForm(forms.ModelForm):
    class Meta:
        model = VehicleType
        fields = ['name']


class CreateUpdateVehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['reg_number', 'brand', 'date_purchase', 'type', 'mileage', 'operation_status']
        widgets = {'date_purchase': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})}
