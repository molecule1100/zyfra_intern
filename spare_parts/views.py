from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import CreateSparePartTypeForm, ReadUpdateSparePartTypeForm, CreateSparePartForm, SparePartImageForm, \
    UpdateSparePartForm, CreateAttributeForm, ReadUpdateAttributeForm
from .models import SparePartType, SparePart, SparePartImage, Attribute, AttributeValue
from django.forms import modelformset_factory


def create_spare_part_type(request):
    form = CreateSparePartTypeForm(request.POST)
    if form.is_valid():
        spare_part_type = form.save(commit=False)
        spare_part_type.created_at = timezone.now()
        spare_part_type.updated_at = timezone.now()
        spare_part_type.is_deleted = False
        spare_part_type.save()
        return redirect('spare_part_type_read_update', pk=spare_part_type.pk)

    return render(request, 'spare_part_type_create.html', {'form': form})


def read_update_spare_part_type(request, pk):
    spare_part_type = get_object_or_404(SparePartType, pk=pk)

    if request.method == 'POST':
        form = ReadUpdateSparePartTypeForm(request.POST, instance=spare_part_type)
        if form.is_valid():
            updated_spare_part_type = form.save(commit=False)
            updated_spare_part_type.updated_at = timezone.now()
            updated_spare_part_type.save()
            return redirect('spare_part_type_read_update', pk=pk)
    else:
        form = ReadUpdateSparePartTypeForm(instance=spare_part_type)

    return render(request, 'spare_part_type_read_update.html', {'form': form, 'spare_part_type': spare_part_type})


def list_delete_spare_part_type(request):
    spare_part_type_list = SparePartType.objects.all().order_by('id')
    paginator = Paginator(spare_part_type_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    pk = request.POST.get('pk')
    if pk:
        spare_part_type = SparePartType.objects.get(pk=pk)
        spare_part_type.delete()

    return render(request, 'spare_part_type_list_delete.html', {'page_obj': page_obj})


SparePartImageFormSet = modelformset_factory(SparePartImage, form=SparePartImageForm, extra=3, can_delete=True)


def create_spare_part(request):
    if request.method == 'POST':
        form = CreateSparePartForm(request.POST)
        formset = SparePartImageFormSet(request.POST, request.FILES, queryset=SparePartImage.objects.none())

        if form.is_valid() and formset.is_valid():
            spare_part = form.save(commit=False)
            spare_part.created_at = timezone.now()
            spare_part.updated_at = timezone.now()
            spare_part.is_deleted = False
            spare_part.save()

            for image_form in formset:
                if image_form.cleaned_data.get('file'):
                    SparePartImage.objects.create(
                        vehicle=spare_part,
                        file=image_form.cleaned_data['file'],
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                        is_deleted=False
                    )

            for attribute in Attribute.objects.filter(is_deleted=False):
                selected = request.POST.get(f'attr_{attribute.id}_selected')
                value = request.POST.get(f'attr_{attribute.id}_value')

                if selected and value:
                    AttributeValue.objects.create(
                        attribute=attribute,
                        spare_part_type=spare_part.spare_part_type,
                        value=value,
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                        is_deleted=False
                    )

            return redirect('spare_part_create')

    else:
        form = CreateSparePartForm()
        formset = SparePartImageFormSet(queryset=SparePartImage.objects.none())

    attributes = Attribute.objects.filter(is_deleted=False)

    context = {
        'form': form,
        'formset': formset,
        'attributes': attributes,
    }

    return render(request, 'spare_part_create.html', context)


def read_spare_part(request, pk):
    spare_part = get_object_or_404(SparePart, pk=pk, is_deleted=False)
    images = SparePartImage.objects.filter(vehicle=spare_part, is_deleted=False)
    attribute_values = AttributeValue.objects.filter(spare_part_type=spare_part.spare_part_type,
                                                     is_deleted=False).select_related('attribute')

    return render(request, 'spare_part_read.html',
                  {'spare_part': spare_part, 'frontend': images, 'attribute_values': attribute_values})


def update_spare_part(request, pk):
    spare_part = get_object_or_404(SparePart, pk=pk, is_deleted=False)

    if request.method == 'POST':
        form = UpdateSparePartForm(request.POST, instance=spare_part)
        formset = SparePartImageFormSet(request.POST, request.FILES,
                                        queryset=SparePartImage.objects.filter(vehicle=spare_part, is_deleted=False))

        if form.is_valid() and formset.is_valid():
            spare_part = form.save(commit=False)
            spare_part.updated_at = timezone.now()
            spare_part.save()

            for image_form in formset:
                if image_form.cleaned_data.get('DELETE'):
                    image = image_form.instance
                    image.is_deleted = True
                    image.save()
                elif image_form.cleaned_data.get('file') and not image_form.instance.pk:
                    SparePartImage.objects.create(
                        vehicle=spare_part,
                        file=image_form.cleaned_data['file'],
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                        is_deleted=False
                    )

            for attribute in Attribute.objects.filter(is_deleted=False):
                selected = request.POST.get(f'attr_{attribute.id}_selected')
                value = request.POST.get(f'attr_{attribute.id}_value')

                existing_attr_value = AttributeValue.objects.filter(attribute=attribute,
                                                                    spare_part_type=spare_part.spare_part_type,
                                                                    is_deleted=False).first()

                if selected and value:
                    if existing_attr_value:
                        existing_attr_value.value = value
                        existing_attr_value.updated_at = timezone.now()
                        existing_attr_value.save()
                    else:
                        AttributeValue.objects.create(
                            attribute=attribute,
                            spare_part_type=spare_part.spare_part_type,
                            value=value,
                            created_at=timezone.now(),
                            updated_at=timezone.now(),
                            is_deleted=False
                        )
                else:
                    if existing_attr_value:
                        existing_attr_value.is_deleted = True
                        existing_attr_value.save()

            return redirect('spare_part_update', pk=spare_part.pk)
    else:
        form = UpdateSparePartForm(instance=spare_part)
        formset = SparePartImageFormSet(queryset=SparePartImage.objects.filter(vehicle=spare_part, is_deleted=False))

    attributes = Attribute.objects.filter(is_deleted=False)
    attribute_values = {}
    for attr_value in AttributeValue.objects.filter(spare_part_type=spare_part.spare_part_type, is_deleted=False):
        attribute_values[attr_value.attribute.id] = attr_value.value

    return render(request, 'spare_part_update.html',
                  {'form': form, 'formset': formset, 'spare_part': spare_part, 'attributes': attributes,
                   'attribute_values': attribute_values})


def list_delete_spare_part(request):
    spare_part_list = SparePart.objects.all()
    paginator = Paginator(spare_part_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    pk = request.POST.get('pk')
    if pk:
        spare_part = SparePart.objects.get(pk=pk)
        spare_part.delete()

    return render(request, 'spare_part_list_delete.html', {'page_obj': page_obj})


def create_attribute(request):
    if request.method == 'POST':
        form = CreateAttributeForm(request.POST)
        if form.is_valid():
            attribute = form.save(commit=False)
            attribute.created_at = timezone.now()
            attribute.updated_at = timezone.now()
            attribute.save()
            return redirect('attribute_list_delete')
    else:
        form = CreateAttributeForm()

    return render(request, 'attribute_create.html', {'form': form})


def read_update_attribute(request, pk):
    attribute = get_object_or_404(Attribute, pk=pk, is_deleted=False)

    if request.method == 'POST':
        form = ReadUpdateAttributeForm(request.POST, instance=attribute)
        if form.is_valid():
            attribute = form.save(commit=False)
            attribute.updated_at = timezone.now()
            attribute.save()
            return redirect('attribute_read_update', pk=attribute.pk)
    else:
        form = CreateAttributeForm(instance=attribute)

    return render(request, 'attribute_read_update.html', {'attribute': attribute,'form': form})


def list_delete_attribute(request):
    attribute_list = Attribute.objects.all()
    paginator = Paginator(attribute_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    pk = request.POST.get('pk')
    if pk:
        attribute = Attribute.objects.get(pk=pk)
        attribute.delete()

    return render(request, 'attribute_list_delete.html', {'page_obj': page_obj})
