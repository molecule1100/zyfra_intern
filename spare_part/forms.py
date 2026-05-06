from django import forms
from django.forms import inlineformset_factory
from spare_part.models import SparePart, SparePartType, SparePartTypeAttribute, Attribute, AttributeValue


class CreateUpdateSparePartTypeForm(forms.ModelForm):
    class Meta:
        model = SparePartType
        fields = ['name']


SparePartTypeAttributeFormSet = inlineformset_factory(
    SparePartType,
    SparePartTypeAttribute,
    fields=['attribute', 'is_required'],
    extra=1,
    can_delete=True,
)


class CreateUpdateSparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = ['spare_part_type', 'vehicle', 'status']


class AttributeValueForm(forms.ModelForm):
    class Meta:
        model = AttributeValue
        fields = ['attribute', 'value']
        widgets = {'attribute': forms.HiddenInput()}


class CreateUpdateAttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ['name', 'unit', 'data_type']
        labels = {'name': 'Название атрибута', 'unit': 'Единица измерения', 'data_type': 'Тип данных'}
