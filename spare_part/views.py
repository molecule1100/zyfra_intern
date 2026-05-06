from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from intern_project.mixins import GroupRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from spare_part.models import SparePart, SparePartType, SparePartImage, Attribute, AttributeValue
from spare_part.forms import CreateUpdateSparePartTypeForm, CreateUpdateSparePartForm, CreateUpdateAttributeForm


class SparePartTypeCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    allowed_groups = ['Администраторы', 'Кладовщики']
    model = SparePartType
    form_class = CreateUpdateSparePartTypeForm
    template_name = 'spare_part/spare_part_type_form.html'
    success_url = reverse_lazy('spare_part:spare-part-type-list')


class SparePartTypeUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    allowed_groups = ['Администраторы', 'Кладовщики']
    model = SparePartType
    form_class = CreateUpdateSparePartTypeForm
    template_name = 'spare_part/spare_part_type_form.html'
    success_url = reverse_lazy('spare_part:spare-part-type-list')


class SparePartTypeListView(LoginRequiredMixin, ListView):
    model = SparePartType
    paginate_by = 10
    template_name = 'spare_part/spare_part_type_list.html'
    success_url = reverse_lazy('spare_part:spare-part-type-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SparePartTypeDeleteView(LoginRequiredMixin, GroupRequiredMixin, View):
    allowed_groups = ['Администраторы', 'Кладовщики']
    success_url = reverse_lazy('spare_part:spare-part-type-list')

    def post(self, request, pk):
        spare_part_type = SparePartType.objects.get(pk=pk)
        spare_part_type.is_deleted = True
        spare_part_type.save()
        return HttpResponseRedirect(self.success_url)


class SparePartCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    allowed_groups = ['Администраторы', 'Кладовщики']
    model = SparePart
    form_class = CreateUpdateSparePartForm
    template_name = 'spare_part/spare_part_form.html'
    success_url = reverse_lazy('spare_part:spare-part-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist('images')
        for image in images:
            SparePartImage.objects.create(spare_part=self.object, file=image)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['active_images'] = self.object.images.filter(is_deleted=False)
        return context


class SparePartDetailView(LoginRequiredMixin, DetailView):
    model = SparePart
    template_name = 'spare_part/spare_part_detail.html'
    success_url = reverse_lazy('spare_part:spare-part-detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['active_images'] = self.object.images.filter(is_deleted=False)
        return context


class SparePartUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    allowed_groups = ['Администраторы', 'Кладовщики']
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
            image = SparePartImage.objects.get(id=delete_image_id, spare_part=self.object)
            image.is_deleted = True
            image.save()
            return redirect(self.request.path)

        form = self.get_form()
        if form.is_valid():
            response = self.form_valid(form)
            images = request.FILES.getlist('images')
            for image_file in images:
                SparePartImage.objects.create(spare_part=self.object, file=image_file)
            return response
        else:
            return self.form_invalid(form)


class SparePartListView(LoginRequiredMixin, ListView):
    model = SparePart
    paginate_by = 10
    template_name = 'spare_part/spare_part_list.html'
    success_url = reverse_lazy('spare_part:spare-part-list')


class SparePartDeleteView(LoginRequiredMixin, GroupRequiredMixin, View):
    allowed_groups = ['Администраторы', 'Кладовщики']
    success_url = reverse_lazy('spare_part:spare-part-list')

    def post(self, request, pk):
        spare_part = SparePart.objects.get(pk=pk)
        spare_part.is_deleted = True
        spare_part.save()
        return HttpResponseRedirect(self.success_url)


class AttributeCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    allowed_groups = ['Администраторы', 'Кладовщики']
    model = Attribute
    form_class = CreateUpdateAttributeForm
    template_name = 'spare_part/attribute_form.html'
    success_url = reverse_lazy('spare_part:attribute-list')


class AttributeUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    allowed_groups = ['Администраторы', 'Кладовщики']
    model = Attribute
    form_class = CreateUpdateAttributeForm
    template_name = 'spare_part/attribute_form.html'
    success_url = reverse_lazy('spare_part:attribute-list')


class AttributeListView(LoginRequiredMixin, ListView):
    model = Attribute
    paginate_by = 5
    template_name = 'spare_part/attribute_list.html'
    success_url = reverse_lazy('spare_part:attribute-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AttributeDetailView(LoginRequiredMixin, DetailView):
    model = Attribute
    template_name = 'spare_part/attribute_detail.html'
    success_url = reverse_lazy('spare_part:attribute-detail')


class AttributeDeleteView(LoginRequiredMixin, GroupRequiredMixin, View):
    allowed_groups = ['Администраторы', 'Кладовщики']
    success_url = reverse_lazy('spare_part:attribute-list')

    def post(self, request, pk):
        attribute = Attribute.objects.get(pk=pk)
        attribute.is_deleted = True
        attribute.save()
        return HttpResponseRedirect(self.success_url)
