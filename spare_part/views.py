from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from spare_part.models import SparePart, SparePartType, SparePartImage, Attribute, AttributeValue
from spare_part.forms import CreateUpdateSparePartTypeForm, CreateUpdateSparePartForm, CreateUpdateAttributeForm


class SparePartTypeCreateView(CreateView):
    model = SparePartType
    form_class = CreateUpdateSparePartTypeForm
    template_name = 'spare_part/spare_part_type_form.html'
    success_url = reverse_lazy('spare_part:spare-part-type-list')


class SparePartTypeUpdateView(UpdateView):
    model = SparePartType
    form_class = CreateUpdateSparePartTypeForm
    template_name = 'spare_part/spare_part_type_form.html'
    success_url = reverse_lazy('spare_part:spare-part-type-list')


class SparePartTypeListView(ListView):
    model = SparePartType
    paginate_by = 10
    template_name = 'spare_part/spare_part_type_list.html'
    success_url = reverse_lazy('spare_part:spare-part-type-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SparePartTypeDeleteView(View):
    success_url = reverse_lazy('spare_part:spare-part-type-list')

    def post(self, request, pk):
        spare_part_type = SparePartType.objects.get(pk=pk)
        spare_part_type.is_deleted = True
        spare_part_type.save()
        return HttpResponseRedirect(self.success_url)


class SparePartCreateView(CreateView):
    model = SparePart
    form_class = CreateUpdateSparePartForm
    template_name = 'spare_part/spare_part_form.html'
    success_url = reverse_lazy('spare_part:spare-part-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist('images')
        for image in images:
            SparePartImage.objects.create(vehicle=self.object, file=image)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['active_images'] = self.object.images.filter(is_deleted=False)
        return context


class SparePartDetailView(DetailView):
    model = SparePart
    template_name = 'spare_part/spare_part_detail.html'
    success_url = reverse_lazy('spare_part:spare-part-detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['active_images'] = self.object.images.filter(is_deleted=False)
        return context


class SparePartUpdateView(UpdateView):
    model = SparePart
    form_class = CreateUpdateSparePartForm
    template_name = 'spare_part/spare_part_form.html'
    success_url = reverse_lazy('spare_part:spare-part-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['active_images'] = self.object.images.filter(is_deleted=False)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        delete_image_id = request.POST.get('delete_image_id')
        if delete_image_id:
            image = SparePartImage.objects.get(id=delete_image_id, vehicle=self.object)
            image.is_deleted = True
            image.save()
            return redirect(self.request.path)

        form = self.get_form()
        if form.is_valid():
            response = self.form_valid(form)
            images = request.FILES.getlist('images')
            for image_file in images:
                SparePartImage.objects.create(vehicle=self.object, file=image_file)
            return response
        else:
            return self.form_invalid(form)


class SparePartListView(ListView):
    model = SparePart
    paginate_by = 10
    template_name = 'spare_part/spare_part_list.html'
    success_url = reverse_lazy('spare_part:spare-part-list')


class SparePartDeleteView(View):
    success_url = reverse_lazy('spare_part:spare-part-list')

    def post(self, request, pk):
        spare_part = SparePart.objects.get(pk=pk)
        spare_part.is_deleted = True
        spare_part.save()
        return HttpResponseRedirect(self.success_url)


class AttributeCreateView(CreateView):
    model = Attribute
    form_class = CreateUpdateAttributeForm
    template_name = 'spare_part/attribute_form.html'
    success_url = reverse_lazy('spare_part:attribute-list')


class AttributeUpdateView(UpdateView):
    model = Attribute
    form_class = CreateUpdateAttributeForm
    template_name = 'spare_part/attribute_form.html'
    success_url = reverse_lazy('spare_part:attribute-list')


class AttributeListView(ListView):
    model = Attribute
    paginate_by = 5
    template_name = 'spare_part/attribute_list.html'
    success_url = reverse_lazy('spare_part:attribute-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AttributeDetailView(DetailView):
    model = Attribute
    template_name = 'spare_part/attribute_detail.html'
    success_url = reverse_lazy('spare_part:attribute-detail')


class AttributeDeleteView(View):
    success_url = reverse_lazy('spare_part:attribute-list')

    def post(self, request, pk):
        attribute = Attribute.objects.get(pk=pk)
        attribute.is_deleted = True
        attribute.save()
        return HttpResponseRedirect(self.success_url)
