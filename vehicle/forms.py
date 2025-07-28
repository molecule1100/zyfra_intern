from django import forms
from .models import VehicleType, Vehicle, VehicleImage


class CreateVehicleTypeForm(forms.ModelForm):
    class Meta:
        model = VehicleType
        fields = ['name']


class ReadUpdateVehicleTypeForm(forms.ModelForm):
    class Meta:
        model = VehicleType
        fields = ['name']


class CreateVehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['reg_number', 'brand', 'type', 'date_purchase', 'mileage', 'operation_status']
        widgets = {
            'operation_status': forms.Select(attrs={'class': 'form-select w-auto'}),
        }
        labels = {
            'reg_number': 'Регистрационный номер',
            'brand': 'Марка',
            'date_purchase': 'Дата покупки',
            'type': 'Тип',
            'mileage': 'Пробег',
            'operation_status': 'Статус работы',
        }


class VehicleImageForm(forms.ModelForm):
    class Meta:
        model = VehicleImage
        fields = ['file']


class UpdateVehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = 'reg_number', 'brand', 'type', 'date_purchase', 'mileage', 'operation_status'
        labels = {
            'reg_number': 'Регистрационный номер',
            'brand': 'Марка',
            'date_purchase': 'Дата покупки',
            'type': 'Тип',
            'mileage': 'Пробег',
            'operation_status': 'Статус работы',
        }
