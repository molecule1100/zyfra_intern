from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from django.urls import reverse

from vehicle.models import Vehicle, VehicleType
from spare_part.models import (SparePart, SparePartType, Attribute, SparePartTypeAttribute,
                                AttributeValue, SparePartInstallation)


def make_vehicle_type():
    return VehicleType.objects.create(name='Экскаватор')


def make_vehicle():
    return Vehicle.objects.create(
        reg_number='Б002ББ99',
        brand='Komatsu',
        date_purchase='2021-01-01',
        type=make_vehicle_type(),
        mileage=500,
        operation_status=Vehicle.OperationStatusChoices.IDLE,
    )


def make_spare_part_type():
    return SparePartType.objects.create(name='Двигатель')


def make_spare_part(spt=None, vehicle=None):
    if spt is None:
        spt = make_spare_part_type()
    return SparePart.objects.create(
        spare_part_type=spt,
        vehicle=vehicle,
        status=SparePart.StatusChoices.IN_STOCK,
    )


def make_user(username, group_name=None, is_superuser=False):
    user = User.objects.create_user(username=username, password='pass123', is_superuser=is_superuser)
    if group_name:
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
    return user


class SparePartModelTest(TestCase):
    def test_str_with_vehicle(self):
        v = make_vehicle()
        sp = make_spare_part(vehicle=v)
        self.assertIn('Двигатель', str(sp))
        self.assertIn('Komatsu', str(sp))

    def test_str_without_vehicle(self):
        sp = make_spare_part()
        self.assertIn('без техники', str(sp))

    def test_create(self):
        sp = make_spare_part()
        self.assertIsNotNone(sp.pk)
        self.assertEqual(sp.status, SparePart.StatusChoices.IN_STOCK)


class AttributeModelTest(TestCase):
    def test_create_attribute(self):
        attr = Attribute.objects.create(name='Мощность', unit='кВт', data_type='number')
        self.assertIsNotNone(attr.pk)

    def test_type_attribute_link(self):
        spt = make_spare_part_type()
        attr = Attribute.objects.create(name='Объём', unit='л', data_type='number')
        SparePartTypeAttribute.objects.create(spare_part_type=spt, attribute=attr)
        self.assertEqual(spt.type_attributes.count(), 1)

    def test_attribute_value_on_spare_part(self):
        spt = make_spare_part_type()
        attr = Attribute.objects.create(name='Масса', unit='кг', data_type='number')
        SparePartTypeAttribute.objects.create(spare_part_type=spt, attribute=attr)
        sp = make_spare_part(spt=spt)
        AttributeValue.objects.create(spare_part=sp, attribute=attr, value='500')
        self.assertEqual(sp.attribute_values.count(), 1)
        self.assertEqual(sp.attribute_values.first().value, '500')


class InstallationTest(TestCase):
    def setUp(self):
        self.user = make_user('mechanic_u', 'Механики')
        self.vehicle = make_vehicle()
        self.spare_part = make_spare_part()

    def test_install_changes_status(self):
        inst = SparePartInstallation.objects.create(
            spare_part=self.spare_part,
            vehicle=self.vehicle,
            installed_by=self.user,
        )
        self.spare_part.vehicle = self.vehicle
        self.spare_part.status = SparePart.StatusChoices.IN_USE
        self.spare_part.save()
        self.spare_part.refresh_from_db()
        self.assertEqual(self.spare_part.status, SparePart.StatusChoices.IN_USE)
        self.assertEqual(self.spare_part.vehicle, self.vehicle)

    def test_uninstall_returns_to_stock(self):
        from django.utils import timezone
        inst = SparePartInstallation.objects.create(
            spare_part=self.spare_part,
            vehicle=self.vehicle,
            installed_by=self.user,
        )
        self.spare_part.vehicle = self.vehicle
        self.spare_part.status = SparePart.StatusChoices.IN_USE
        self.spare_part.save()
        inst.uninstalled_at = timezone.now()
        inst.uninstalled_by = self.user
        inst.save()
        self.spare_part.vehicle = None
        self.spare_part.status = SparePart.StatusChoices.IN_STOCK
        self.spare_part.save()
        self.spare_part.refresh_from_db()
        self.assertEqual(self.spare_part.status, SparePart.StatusChoices.IN_STOCK)
        self.assertIsNone(self.spare_part.vehicle)


class SparePartViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = make_user('admin_u', is_superuser=True)
        self.storekeeper = make_user('store_u', 'Кладовщики')
        self.mechanic = make_user('mech_u', 'Механики')

    def test_list_requires_login(self):
        resp = self.client.get(reverse('spare_part:spare-part-list'))
        self.assertEqual(resp.status_code, 302)

    def test_list_accessible_to_storekeeper(self):
        self.client.login(username='store_u', password='pass123')
        resp = self.client.get(reverse('spare_part:spare-part-list'))
        self.assertEqual(resp.status_code, 200)

    def test_create_allowed_for_storekeeper(self):
        self.client.login(username='store_u', password='pass123')
        resp = self.client.get(reverse('spare_part:spare-part-create'))
        self.assertEqual(resp.status_code, 200)

    def test_create_forbidden_for_mechanic(self):
        self.client.login(username='mech_u', password='pass123')
        resp = self.client.get(reverse('spare_part:spare-part-create'))
        self.assertEqual(resp.status_code, 403)

    def test_deleted_hidden_by_default(self):
        sp = make_spare_part()
        sp.is_deleted = True
        sp.save()
        self.client.login(username='admin_u', password='pass123')
        resp = self.client.get(reverse('spare_part:spare-part-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, f'spare-part-detail/{sp.pk}')
