from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from intern_project.mixins import GroupRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

import logging
from django.db import transaction
from django.utils import timezone

from spare_part.models import (SparePart, SparePartType, SparePartImage, Attribute, AttributeValue,
                                SparePartTypeAttribute, SparePartInstallation)
from spare_part.forms import (CreateUpdateSparePartTypeForm, CreateUpdateSparePartForm,
                               CreateUpdateAttributeForm, SparePartTypeAttributeFormSet, AttributeValueForm)

logger = logging.getLogger('spare_part')


class SparePartTypeCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    allowed_groups = ['Администраторы', 'Кладовщики']
    model = SparePartType
    form_class = CreateUpdateSparePartTypeForm
    template_name = 'spare_part/spare_part_type_form.html'
    success_url = reverse_lazy('spare_part:spare-part-type-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['attr_formset'] = SparePartTypeAttributeFormSet(self.request.POST, instance=self.object)
        else:
            context['attr_formset'] = SparePartTypeAttributeFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        attr_formset = context['attr_formset']
        self.object = form.save()
        if attr_formset.is_valid():
            attr_formset.instance = self.object
            attr_formset.save()
        return redirect(self.success_url)


class SparePartTypeUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    allowed_groups = ['Администраторы', 'Кладовщики']
    model = SparePartType
    form_class = CreateUpdateSparePartTypeForm
    template_name = 'spare_part/spare_part_type_form.html'
    success_url = reverse_lazy('spare_part:spare-part-type-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['attr_formset'] = SparePartTypeAttributeFormSet(self.request.POST, instance=self.object)
        else:
            context['attr_formset'] = SparePartTypeAttributeFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        attr_formset = context['attr_formset']
        self.object = form.save()
        if attr_formset.is_valid():
            attr_formset.instance = self.object
            attr_formset.save()
        return redirect(self.success_url)


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
            context['attribute_values'] = self.object.attribute_values.filter(is_deleted=False).select_related('attribute')
            context['installations'] = self.object.installations.select_related('vehicle', 'installed_by', 'uninstalled_by')
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
            type_attributes = []
            if self.object.spare_part_type:
                type_attributes = self.object.spare_part_type.type_attributes.filter(
                    is_deleted=False
                ).select_related('attribute')
            attr_forms = []
            for ta in type_attributes:
                existing = self.object.attribute_values.filter(attribute=ta.attribute).first()
                form = AttributeValueForm(
                    self.request.POST or None,
                    instance=existing,
                    prefix=f'attr_{ta.attribute.pk}',
                    initial={'attribute': ta.attribute},
                )
                attr_forms.append((ta.attribute, form))
            context['attr_forms'] = attr_forms
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
            if self.object.spare_part_type:
                type_attributes = self.object.spare_part_type.type_attributes.filter(
                    is_deleted=False
                ).select_related('attribute')
                for ta in type_attributes:
                    existing = self.object.attribute_values.filter(attribute=ta.attribute).first()
                    av_form = AttributeValueForm(
                        request.POST,
                        instance=existing,
                        prefix=f'attr_{ta.attribute.pk}',
                        initial={'attribute': ta.attribute},
                    )
                    if av_form.is_valid() and av_form.cleaned_data.get('value'):
                        av = av_form.save(commit=False)
                        av.spare_part = self.object
                        av.attribute = ta.attribute
                        av.save()
            return response
        return self.form_invalid(form)


class SparePartListView(LoginRequiredMixin, ListView):
    model = SparePart
    paginate_by = 10
    template_name = 'spare_part/spare_part_list.html'
    success_url = reverse_lazy('spare_part:spare-part-list')

    def get_queryset(self):
        queryset = SparePart.objects.all()
        show_deleted = self.request.GET.get('show_deleted')
        if not show_deleted:
            queryset = queryset.filter(is_deleted=False)
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        spare_part_type = self.request.GET.get('type')
        if spare_part_type:
            queryset = queryset.filter(spare_part_type__id=spare_part_type)
        vehicle_search = self.request.GET.get('vehicle')
        if vehicle_search:
            queryset = queryset.filter(
                vehicle__reg_number__icontains=vehicle_search
            ) | queryset.filter(
                vehicle__brand__icontains=vehicle_search
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', '')
        context['current_type'] = self.request.GET.get('type', '')
        context['current_vehicle'] = self.request.GET.get('vehicle', '')
        context['show_deleted'] = self.request.GET.get('show_deleted', '')
        context['spare_part_types'] = SparePartType.objects.filter(is_deleted=False)
        context['status_choices'] = SparePart.StatusChoices.choices
        return context


class SparePartDeleteView(LoginRequiredMixin, GroupRequiredMixin, View):
    allowed_groups = ['Администраторы', 'Кладовщики']
    success_url = reverse_lazy('spare_part:spare-part-list')

    def post(self, request, pk):
        spare_part = SparePart.objects.get(pk=pk)
        spare_part.is_deleted = True
        spare_part.save()
        logger.info(f'Запчасть {spare_part} удалена пользователем {request.user}')
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


class SparePartInstallView(LoginRequiredMixin, GroupRequiredMixin, View):
    allowed_groups = ['Администраторы', 'Механики']

    def get(self, request, pk):
        from django.shortcuts import get_object_or_404, render
        from vehicle.models import Vehicle
        spare_part = get_object_or_404(SparePart, pk=pk)
        vehicles = Vehicle.objects.filter(is_deleted=False)
        return render(request, 'spare_part/spare_part_install.html', {
            'spare_part': spare_part,
            'vehicles': vehicles,
        })

    def post(self, request, pk):
        from django.shortcuts import get_object_or_404
        from vehicle.models import Vehicle
        spare_part = get_object_or_404(SparePart, pk=pk)
        vehicle_id = request.POST.get('vehicle')
        notes = request.POST.get('notes', '')
        with transaction.atomic():
            vehicle = Vehicle.objects.get(pk=vehicle_id)
            SparePartInstallation.objects.create(
                spare_part=spare_part,
                vehicle=vehicle,
                installed_by=request.user,
                notes=notes,
            )
            spare_part.vehicle = vehicle
            spare_part.status = SparePart.StatusChoices.IN_USE
            spare_part.save()
        logger.info(f'Запчасть {spare_part} установлена на {vehicle} пользователем {request.user}')
        return redirect('spare_part:spare-part-detail', pk=spare_part.pk)


class SparePartUninstallView(LoginRequiredMixin, GroupRequiredMixin, View):
    allowed_groups = ['Администраторы', 'Механики']

    def post(self, request, pk):
        from django.shortcuts import get_object_or_404
        spare_part = get_object_or_404(SparePart, pk=pk)
        with transaction.atomic():
            active = spare_part.installations.filter(uninstalled_at__isnull=True).first()
            if active:
                active.uninstalled_at = timezone.now()
                active.uninstalled_by = request.user
                active.save()
            spare_part.vehicle = None
            spare_part.status = SparePart.StatusChoices.IN_STOCK
            spare_part.save()
        logger.info(f'Запчасть {spare_part} снята пользователем {request.user}')
        return redirect('spare_part:spare-part-detail', pk=spare_part.pk)
