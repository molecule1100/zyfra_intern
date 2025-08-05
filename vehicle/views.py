from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Vehicle, VehicleType
from .forms import CreateUpdateVehicleTypeForm, CreateUpdateVehicleForm


class VehicleTypeCreateView(CreateView):
    model = VehicleType
    form_class = CreateUpdateVehicleTypeForm
    template_name = 'vehicle/vehicletype_form.html'
    success_url = reverse_lazy('vehicle-type-list')


class VehicleTypeUpdateView(UpdateView):
    model = VehicleType
    form_class = CreateUpdateVehicleTypeForm
    template_name = 'vehicle/vehicletype_form.html'
    success_url = reverse_lazy('vehicle-type-list')


class VehicleTypeListView(ListView):
    model = VehicleType
    paginate_by = 10
    template_name = 'vehicle/vehicletype_list.html'
    success_url = reverse_lazy('vehicle-type-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class VehicleTypeDeleteView(DeleteView):
    models = VehicleType
    queryset = VehicleType.objects.all()
    template_name = 'vehicle/vehicletype_delete.html'
    success_url = reverse_lazy('vehicle-type-list')

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        object.is_deleted = True
        object.save()
        return HttpResponseRedirect(self.success_url)


class VehicleCreateView(CreateView):
    model = Vehicle
    form_class = CreateUpdateVehicleForm
    template_name = 'vehicle/vehicle_form.html'
    success_url = reverse_lazy('vehicle-list')


class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'vehicle/vehicle_detail.html'
    success_url = reverse_lazy('vehicle-detail')


class VehicleUpdateView(UpdateView):
    model = Vehicle
    form_class = CreateUpdateVehicleForm
    template_name = 'vehicle/vehicle_form.html'
    success_url = reverse_lazy('vehicle-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class VehicleListView(ListView):
    model = Vehicle
    paginate_by = 10
    template_name = 'vehicle/vehicle_list.html'
    success_url = reverse_lazy('vehicle-list')

    def get_queryset(self):
        queryset = Vehicle.objects.all()
        brand = self.request.GET.get('brand')
        if brand:
            queryset = queryset.filter(brand__icontains=brand)
        return queryset


class VehicleDeleteView(DeleteView):
    models = Vehicle
    queryset = Vehicle.objects.all()
    template_name = 'vehicle/vehicle_delete.html'
    success_url = reverse_lazy('vehicle-list')

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        object.is_deleted = True
        object.save()
        return HttpResponseRedirect(self.success_url)
