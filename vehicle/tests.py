from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from django.urls import reverse

from vehicle.models import Vehicle, VehicleType


def make_vehicle_type():
    return VehicleType.objects.create(name='Бульдозер')


def make_vehicle(vehicle_type=None):
    if vehicle_type is None:
        vehicle_type = make_vehicle_type()
    return Vehicle.objects.create(
        reg_number='А001АА99',
        brand='Caterpillar',
        date_purchase='2020-01-01',
        type=vehicle_type,
        mileage=1000,
        operation_status=Vehicle.OperationStatusChoices.IN_USE,
    )


def make_user(username, group_name=None, is_superuser=False):
    user = User.objects.create_user(username=username, password='pass123', is_superuser=is_superuser)
    if group_name:
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
    return user


class VehicleModelTest(TestCase):
    def test_str(self):
        v = make_vehicle()
        self.assertEqual(str(v), 'Caterpillar (А001АА99)')

    def test_soft_delete(self):
        v = make_vehicle()
        v.is_deleted = True
        v.save()
        self.assertTrue(Vehicle.objects.get(pk=v.pk).is_deleted)

    def test_create(self):
        v = make_vehicle()
        self.assertIsNotNone(v.pk)
        self.assertEqual(v.brand, 'Caterpillar')


class VehicleViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = make_user('admin_u', is_superuser=True)
        self.mechanic = make_user('mechanic_u', 'Механики')
        self.storekeeper = make_user('store_u', 'Кладовщики')

    def test_list_requires_login(self):
        resp = self.client.get(reverse('vehicle:vehicle-list'))
        self.assertRedirects(resp, '/accounts/login/?next=/vehicle/vehicles/')

    def test_list_accessible_to_authenticated(self):
        self.client.login(username='admin_u', password='pass123')
        resp = self.client.get(reverse('vehicle:vehicle-list'))
        self.assertEqual(resp.status_code, 200)

    def test_create_allowed_for_mechanic(self):
        self.client.login(username='mechanic_u', password='pass123')
        resp = self.client.get(reverse('vehicle:vehicle-create'))
        self.assertEqual(resp.status_code, 200)

    def test_create_forbidden_for_storekeeper(self):
        self.client.login(username='store_u', password='pass123')
        resp = self.client.get(reverse('vehicle:vehicle-create'))
        self.assertEqual(resp.status_code, 403)

    def test_filter_by_brand(self):
        make_vehicle()
        self.client.login(username='admin_u', password='pass123')
        resp = self.client.get(reverse('vehicle:vehicle-list') + '?brand=Caterpillar')
        self.assertContains(resp, 'Caterpillar')

    def test_filter_by_status(self):
        make_vehicle()
        self.client.login(username='admin_u', password='pass123')
        resp = self.client.get(reverse('vehicle:vehicle-list') + '?status=1')
        self.assertEqual(resp.status_code, 200)

    def test_deleted_hidden_by_default(self):
        v = make_vehicle()
        v.is_deleted = True
        v.save()
        self.client.login(username='admin_u', password='pass123')
        resp = self.client.get(reverse('vehicle:vehicle-list'))
        self.assertNotContains(resp, v.reg_number)
