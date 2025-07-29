from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateVehicleTypeForm, ReadUpdateVehicleTypeForm, CreateVehicleForm, VehicleImageForm, \
    UpdateVehicleForm
from django.utils import timezone
from django.forms import modelformset_factory
from .models import VehicleType, Vehicle, VehicleImage
from django.core.paginator import Paginator


def create_vehicle_type(request):
    form = CreateVehicleTypeForm(request.POST)
    if form.is_valid():
        vehicle_type = form.save(commit=False)
        vehicle_type.created_at = timezone.now()
        vehicle_type.updated_at = timezone.now()
        vehicle_type.is_deleted = False
        vehicle_type.save()
        return redirect('vehicle_type_read_update', pk=vehicle_type.pk)

    return render(request, 'vehicle_type_create.html', {'form': form})


def read_update_vehicle_type(request, pk):
    vehicle_type = get_object_or_404(VehicleType, pk=pk)

    if request.method == 'POST':
        form = ReadUpdateVehicleTypeForm(request.POST, instance=vehicle_type)
        if form.is_valid():
            updated_vehicle_type = form.save(commit=False)
            updated_vehicle_type.updated_at = timezone.now()
            updated_vehicle_type.save()
            return redirect('vehicle_type_read_update', pk=pk)
    else:
        form = ReadUpdateVehicleTypeForm(instance=vehicle_type)

    return render(request, 'vehicle_type_read_update.html', {'form': form, 'vehicle_type': vehicle_type})


def list_delete_vehicle_type(request):
    vehicle_type_list = VehicleType.objects.all().order_by('id')
    paginator = Paginator(vehicle_type_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    pk = request.POST.get('pk')
    if pk:
        vehicle_type = VehicleType.objects.get(pk=pk)
        vehicle_type.delete()

    return render(request, 'vehicle_type_list_delete.html', {'page_obj': page_obj})


VehicleImageFormSet = modelformset_factory(VehicleImage, form=VehicleImageForm, extra=1, can_delete=True)


def create_vehicle(request):
    if request.method == 'POST':
        form = CreateVehicleForm(request.POST)
        formset = VehicleImageFormSet(request.POST, request.FILES, queryset=VehicleImage.objects.none())

        if form.is_valid() and formset.is_valid():
            vehicle = form.save(commit=False)
            vehicle.created_at = timezone.now()
            vehicle.updated_at = timezone.now()
            vehicle.date_purchase = timezone.now().date()
            vehicle.is_deleted = False
            vehicle.save()

            for image_form in formset:
                if image_form.cleaned_data.get('file'):
                    VehicleImage.objects.create(
                        vehicle=vehicle,
                        file=image_form.cleaned_data['file'],
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                        is_deleted=False
                    )

            return redirect('vehicle_read', pk=vehicle.pk)

    else:
        form = CreateVehicleForm()
        formset = VehicleImageFormSet(queryset=VehicleImage.objects.none())

    return render(request, 'vehicle_create.html', {'form': form, 'formset': formset})


def read_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, is_deleted=False)
    images = VehicleImage.objects.filter(vehicle=vehicle, is_deleted=False)
    return render(request, 'vehicle_read.html', {'vehicle': vehicle, 'frontend': images})


def list_delete_vehicle(request):
    vehicle_list = Vehicle.objects.all()
    paginator = Paginator(vehicle_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    pk = request.POST.get('pk')
    if pk:
        vehicle = Vehicle.objects.get(pk=pk)
        vehicle.delete()

    return render(request, 'vehicle_list_delete.html', {'page_obj': page_obj})


def update_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)

    if request.method == 'POST':
        form = UpdateVehicleForm(request.POST, instance=vehicle)
        formset = VehicleImageFormSet(request.POST, request.FILES,
                                      queryset=VehicleImage.objects.filter(vehicle=vehicle, is_deleted=False))
        if form.is_valid() and formset.is_valid():
            vehicle = form.save(commit=False)
            vehicle.updated_at = timezone.now()
            vehicle.save()

            for image_form in formset:
                if image_form.cleaned_data.get('DELETE'):
                    image = image_form.instance
                    image.is_deleted = True
                    image.save()
                elif image_form.cleaned_data.get('file') and not image_form.instance.pk:
                    VehicleImage.objects.create(
                        vehicle=vehicle,
                        file=image_form.cleaned_data['file'],
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                        is_deleted=False
                    )
            return redirect('vehicle_update', pk=vehicle.pk)
    else:
        form = UpdateVehicleForm(instance=vehicle)
        formset = VehicleImageFormSet(queryset=VehicleImage.objects.filter(vehicle=vehicle, is_deleted=False))

    return render(request, 'vehicle_update.html', {'form': form, 'formset': formset,
                                                        'vehicle': vehicle})
