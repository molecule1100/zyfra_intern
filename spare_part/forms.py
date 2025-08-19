from django import forms
from spare_part.models import SparePart, SparePartType, Attribute


class CreateUpdateSparePartTypeForm(forms.ModelForm):
    class Meta:
        model = SparePartType
        fields = ['name']


class CreateUpdateSparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = ['spare_part_type', 'vehicle', 'status']


class CreateUpdateAttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ['name', 'unit', 'data_type']
        labels = {'name': 'Название атрибута', 'unit': 'Единица измерения', 'data_type': 'Тип данных'}
