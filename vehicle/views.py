from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from intern_project.mixins import GroupRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from vehicle.models import Vehicle, VehicleType, VehicleImage
from vehicle.forms import CreateUpdateVehicleTypeForm, CreateUpdateVehicleForm


class VehicleTypeCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    allowed_groups = ['Администраторы', 'Механики']
    model = VehicleType
    form_class = CreateUpdateVehicleTypeForm
    template_name = 'vehicle/vehicletype_form.html'
    success_url = reverse_lazy('vehicle:vehicle-type-list')


class VehicleTypeUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    allowed_groups = ['Администраторы', 'Механики']
    model = VehicleType
    form_class = CreateUpdateVehicleTypeForm
    template_name = 'vehicle/vehicletype_form.html'
    success_url = reverse_lazy('vehicle:vehicle-type-list')


class VehicleTypeListView(LoginRequiredMixin, ListView):
    model = VehicleType
    paginate_by = 10
    template_name = 'vehicle/vehicletype_list.html'
    success_url = reverse_lazy('vehicle:vehicle-type-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class VehicleTypeDeleteView(LoginRequiredMixin, GroupRequiredMixin, View):
    allowed_groups = ['Администраторы', 'Механики']
    success_url = reverse_lazy('vehicle:vehicle-type-list')

    def post(self, request, pk):
        vehicle_type = VehicleType.objects.get(pk=pk)
        vehicle_type.is_deleted = True
        vehicle_type.save()
        return HttpResponseRedirect(self.success_url)


class VehicleCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    allowed_groups = ['Администраторы', 'Механики']
    model = Vehicle
    form_class = CreateUpdateVehicleForm
    template_name = 'vehicle/vehicle_form.html'
    success_url = reverse_lazy('vehicle:vehicle-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist('images')
        for image in images:
            VehicleImage.objects.create(vehicle=self.object, file=image)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['active_images'] = self.object.images.filter(is_deleted=False)
        return context


class VehicleDetailView(LoginRequiredMixin, DetailView):
    model = Vehicle
    template_name = 'vehicle/vehicle_detail.html'
    success_url = reverse_lazy('vehicle:vehicle-detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['active_images'] = self.object.images.filter(is_deleted=False)
        return context


class VehicleUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    allowed_groups = ['Администраторы', 'Механики']
    model = Vehicle
    form_class = CreateUpdateVehicleForm
    template_name = 'vehicle/vehicle_form.html'
    success_url = reverse_lazy('vehicle:vehicle-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['active_images'] = self.object.images.filter(is_deleted=False)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        delete_image_id = request.POST.get('delete_image_id')
        if delete_image_id:
            image = VehicleImage.objects.get(id=delete_image_id, vehicle=self.object)
            image.is_deleted = True
            image.save()
            return redirect(self.request.path)

        form = self.get_form()
        if form.is_valid():
            response = self.form_valid(form)
            images = request.FILES.getlist('images')
            for image_file in images:
                VehicleImage.objects.create(vehicle=self.object, file=image_file)
            return response
        else:
            return self.form_invalid(form)


class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    paginate_by = 10
    template_name = 'vehicle/vehicle_list.html'
    success_url = reverse_lazy('vehicle:vehicle-list')

    def get_queryset(self):
        queryset = Vehicle.objects.all()
        brand = self.request.GET.get('brand')
        if brand:
            queryset = queryset.filter(brand__icontains=brand)
        return queryset


class VehicleDeleteView(LoginRequiredMixin, GroupRequiredMixin, View):
    allowed_groups = ['Администраторы', 'Механики']
    success_url = reverse_lazy('vehicle:vehicle-list')

    def post(self, request, pk):
        vehicle = Vehicle.objects.get(pk=pk)
        vehicle.is_deleted = True
        vehicle.save()
        return HttpResponseRedirect(self.success_url)
