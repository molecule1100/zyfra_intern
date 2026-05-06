from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from django.urls import reverse

from vehicle.models import Vehicle, VehicleType
from spare_part.models import SparePart, SparePartType


def make_user(username, group_name=None, is_superuser=False):
    user = User.objects.create_user(username=username, password='pass123', is_superuser=is_superuser)
    if group_name:
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
    return user


def make_vehicle(status, brand='Caterpillar', idx=0):
    vt, _ = VehicleType.objects.get_or_create(name='Бульдозер')
    return Vehicle.objects.create(
        reg_number=f'А{idx:03d}АА99',
        brand=brand,
        date_purchase='2020-01-01',
        type=vt,
        mileage=1000,
        operation_status=status,
    )


class DashboardTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = make_user('admin_u', is_superuser=True)
        self.mechanic = make_user('mech_u', 'Механики')
        self.storekeeper = make_user('store_u', 'Кладовщики')
        for i in range(3):
            make_vehicle(Vehicle.OperationStatusChoices.IN_USE, idx=i)
        for i in range(3, 5):
            make_vehicle(Vehicle.OperationStatusChoices.REPAIR, idx=i)

    def test_dashboard_accessible_to_admin(self):
        self.client.login(username='admin_u', password='pass123')
        resp = self.client.get(reverse('reports:dashboard'))
        self.assertEqual(resp.status_code, 200)

    def test_dashboard_accessible_to_mechanic(self):
        self.client.login(username='mech_u', password='pass123')
        resp = self.client.get(reverse('reports:dashboard'))
        self.assertEqual(resp.status_code, 200)

    def test_dashboard_forbidden_for_storekeeper(self):
        self.client.login(username='store_u', password='pass123')
        resp = self.client.get(reverse('reports:dashboard'))
        self.assertEqual(resp.status_code, 403)

    def test_vehicle_total_count(self):
        self.client.login(username='admin_u', password='pass123')
        resp = self.client.get(reverse('reports:dashboard'))
        self.assertEqual(resp.context['vehicle_total'], 5)

    def test_vehicles_in_repair_count(self):
        self.client.login(username='admin_u', password='pass123')
        resp = self.client.get(reverse('reports:dashboard'))
        self.assertEqual(len(resp.context['vehicles_in_repair']), 2)

    def test_requires_login(self):
        resp = self.client.get(reverse('reports:dashboard'))
        self.assertEqual(resp.status_code, 302)
