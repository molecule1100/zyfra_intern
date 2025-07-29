from django import forms
from .models import SparePartType, SparePart, SparePartImage, Attribute


class CreateSparePartTypeForm(forms.ModelForm):
    class Meta:
        model = SparePartType
        fields = ['name']


class ReadUpdateSparePartTypeForm(forms.ModelForm):
    class Meta:
        model = SparePartType
        fields = ['name']


class CreateSparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = ['spare_part_type', 'vehicle', 'status']


class SparePartImageForm(forms.ModelForm):
    class Meta:
        model = SparePartImage
        fields = ['file']


class UpdateSparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = ['spare_part_type', 'vehicle', 'status']


class CreateAttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ['name', 'unit', 'data_type']
        labels = {
            'name': 'Название атрибута',
            'unit': 'Единица измерения',
            'data_type': 'Тип данных',
        }


class ReadUpdateAttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ['name', 'unit', 'data_type']
        labels = {
            'name': 'Название атрибута',
            'unit': 'Единица измерения',
            'data_type': 'Тип данных',
        }


