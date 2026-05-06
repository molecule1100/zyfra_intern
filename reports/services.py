from django.db.models import Count

from vehicle.models import Vehicle
from spare_part.models import SparePart


def get_vehicle_stats():
    return Vehicle.objects.filter(is_deleted=False).values(
        'operation_status'
    ).annotate(count=Count('id'))


def get_spare_part_stats():
    return SparePart.objects.filter(is_deleted=False).values(
        'status', 'spare_part_type__name'
    ).annotate(count=Count('id'))


def get_vehicles_in_repair():
    return Vehicle.objects.filter(
        operation_status=Vehicle.OperationStatusChoices.REPAIR,
        is_deleted=False,
    )


def get_spare_parts_waiting_repair():
    return SparePart.objects.filter(
        status=SparePart.StatusChoices.WAITING_REPAIR,
        is_deleted=False,
    ).select_related('spare_part_type', 'vehicle')


def get_top_brands(limit=5):
    return Vehicle.objects.filter(is_deleted=False).values('brand').annotate(
        count=Count('id')
    ).order_by('-count')[:limit]
