from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from intern_project.mixins import GroupRequiredMixin
from vehicle.models import Vehicle
from spare_part.models import SparePart
from reports.services import (get_vehicle_stats, get_spare_part_stats, get_vehicles_in_repair,
                               get_spare_parts_waiting_repair, get_top_brands)


class DashboardView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    allowed_groups = ['Администраторы', 'Механики']
    template_name = 'reports/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicle_total'] = Vehicle.objects.filter(is_deleted=False).count()
        context['spare_part_total'] = SparePart.objects.filter(is_deleted=False).count()
        context['vehicle_stats'] = get_vehicle_stats()
        context['spare_part_stats'] = get_spare_part_stats()
        context['vehicles_in_repair'] = get_vehicles_in_repair()
        context['spare_parts_waiting_repair'] = get_spare_parts_waiting_repair()
        context['top_brands'] = get_top_brands()
        return context
