import os
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from vehicle.models import VehicleType, Vehicle
from spare_part.models import (SparePartType, SparePart, Attribute, SparePartTypeAttribute,
                                AttributeValue, SparePartInstallation)
from spare_part.management.commands.setup_groups import setup_groups


class Command(BaseCommand):
    help = 'Наполнить БД демо-данными (идемпотентно)'

    def handle(self, *args, **options):
        setup_groups()

        password = os.environ.get('DEMO_PASSWORD', 'demo12345')

        admin, _ = User.objects.get_or_create(username='admin')
        admin.set_password(password)
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()

        from django.contrib.auth.models import Group
        storekeeper_group, _ = Group.objects.get_or_create(name='Кладовщики')
        mechanic_group, _ = Group.objects.get_or_create(name='Механики')

        storekeeper, _ = User.objects.get_or_create(username='storekeeper1')
        storekeeper.set_password(password)
        storekeeper.save()
        storekeeper.groups.set([storekeeper_group])

        mechanic, _ = User.objects.get_or_create(username='mechanic1')
        mechanic.set_password(password)
        mechanic.save()
        mechanic.groups.set([mechanic_group])

        vt_data = ['Бульдозер', 'Экскаватор', 'Кран', 'Самосвал']
        vehicle_types = {}
        for name in vt_data:
            vt, _ = VehicleType.objects.get_or_create(name=name)
            vehicle_types[name] = vt

        vehicles_data = [
            ('А001АА99', 'Caterpillar', Vehicle.OperationStatusChoices.IN_USE, 'Бульдозер'),
            ('Б002ББ99', 'Komatsu', Vehicle.OperationStatusChoices.IDLE, 'Экскаватор'),
            ('В003ВВ99', 'Hitachi', Vehicle.OperationStatusChoices.REPAIR, 'Кран'),
            ('Г004ГГ99', 'JCB', Vehicle.OperationStatusChoices.IN_USE, 'Самосвал'),
            ('Д005ДД99', 'Caterpillar', Vehicle.OperationStatusChoices.IDLE, 'Экскаватор'),
            ('Е006ЕЕ99', 'Komatsu', Vehicle.OperationStatusChoices.IN_USE, 'Бульдозер'),
            ('Ж007ЖЖ99', 'Hitachi', Vehicle.OperationStatusChoices.REPAIR, 'Кран'),
            ('З008ЗЗ99', 'JCB', Vehicle.OperationStatusChoices.IN_USE, 'Самосвал'),
        ]
        vehicles = {}
        for reg, brand, status, vtype in vehicles_data:
            v, _ = Vehicle.objects.get_or_create(
                reg_number=reg,
                defaults={
                    'brand': brand,
                    'date_purchase': '2020-01-01',
                    'type': vehicle_types[vtype],
                    'mileage': 1000,
                    'operation_status': status,
                },
            )
            vehicles[reg] = v

        spt_data = ['Двигатель', 'Гидравлический насос', 'Гусеница', 'Топливный фильтр', 'Аккумулятор']
        spare_part_types = {}
        for name in spt_data:
            spt, _ = SparePartType.objects.get_or_create(name=name)
            spare_part_types[name] = spt

        attrs_data = [
            ('Мощность', 'кВт', 'number'),
            ('Масса', 'кг', 'number'),
            ('Производитель', '', 'string'),
            ('Серийный номер', '', 'string'),
        ]
        attrs = {}
        for name, unit, dtype in attrs_data:
            attr, _ = Attribute.objects.get_or_create(name=name, defaults={'unit': unit, 'data_type': dtype})
            attrs[name] = attr

        type_attr_map = {
            'Двигатель': ['Мощность', 'Масса', 'Производитель', 'Серийный номер'],
            'Гидравлический насос': ['Мощность', 'Масса', 'Производитель'],
            'Гусеница': ['Масса', 'Производитель'],
            'Топливный фильтр': ['Производитель', 'Серийный номер'],
            'Аккумулятор': ['Мощность', 'Производитель'],
        }
        for spt_name, attr_names in type_attr_map.items():
            spt = spare_part_types[spt_name]
            for attr_name in attr_names:
                SparePartTypeAttribute.objects.get_or_create(
                    spare_part_type=spt,
                    attribute=attrs[attr_name],
                )

        spare_parts_data = [
            ('Двигатель', SparePart.StatusChoices.IN_USE, 'А001АА99',
             [('Мощность', '250'), ('Масса', '800'), ('Производитель', 'Cummins'), ('Серийный номер', 'SN001')]),
            ('Двигатель', SparePart.StatusChoices.IN_STOCK, None,
             [('Мощность', '300'), ('Масса', '900'), ('Производитель', 'Perkins'), ('Серийный номер', 'SN002')]),
            ('Гидравлический насос', SparePart.StatusChoices.IN_USE, 'Б002ББ99',
             [('Мощность', '75'), ('Масса', '50'), ('Производитель', 'Bosch')]),
            ('Гусеница', SparePart.StatusChoices.IN_STOCK, None,
             [('Масса', '200'), ('Производитель', 'Caterpillar')]),
            ('Топливный фильтр', SparePart.StatusChoices.IN_USE, 'В003ВВ99',
             [('Производитель', 'Fleetguard'), ('Серийный номер', 'FF5612')]),
            ('Топливный фильтр', SparePart.StatusChoices.WAITING_REPAIR, 'Г004ГГ99',
             [('Производитель', 'Mann'), ('Серийный номер', 'WK940')]),
            ('Аккумулятор', SparePart.StatusChoices.IN_USE, 'Д005ДД99',
             [('Мощность', '12'), ('Производитель', 'Varta')]),
            ('Аккумулятор', SparePart.StatusChoices.IN_STOCK, None,
             [('Мощность', '24'), ('Производитель', 'Bosch')]),
            ('Гидравлический насос', SparePart.StatusChoices.REPAIR, None,
             [('Мощность', '55'), ('Масса', '40'), ('Производитель', 'Parker')]),
            ('Гусеница', SparePart.StatusChoices.IN_USE, 'Е006ЕЕ99',
             [('Масса', '250'), ('Производитель', 'Komatsu')]),
        ]

        created_parts = []
        for idx, (spt_name, status, vehicle_reg, av_data) in enumerate(spare_parts_data):
            spt = spare_part_types[spt_name]
            vehicle = vehicles.get(vehicle_reg) if vehicle_reg else None
            existing = SparePart.objects.filter(spare_part_type=spt, status=status).exclude(
                pk__in=[sp.pk for sp in created_parts]
            ).first()
            if existing:
                sp = existing
            else:
                sp = SparePart.objects.create(spare_part_type=spt, vehicle=vehicle, status=status)
            for attr_name, value in av_data:
                AttributeValue.objects.get_or_create(
                    spare_part=sp,
                    attribute=attrs[attr_name],
                    defaults={'value': value},
                )
            created_parts.append(sp)

        installations_data = [
            (created_parts[0], vehicles['А001АА99']),
            (created_parts[2], vehicles['Б002ББ99']),
            (created_parts[4], vehicles['В003ВВ99']),
            (created_parts[6], vehicles['Д005ДД99']),
            (created_parts[9], vehicles['Е006ЕЕ99']),
        ]
        for sp, v in installations_data:
            if not sp.installations.filter(uninstalled_at__isnull=True).exists():
                SparePartInstallation.objects.create(
                    spare_part=sp,
                    vehicle=v,
                    installed_by=mechanic,
                )

        uninstall_data = [
            (created_parts[5], vehicles['Г004ГГ99']),
        ]
        for sp, v in uninstall_data:
            if not sp.installations.exists():
                inst = SparePartInstallation.objects.create(
                    spare_part=sp,
                    vehicle=v,
                    installed_by=mechanic,
                )
                inst.uninstalled_at = timezone.now()
                inst.uninstalled_by = mechanic
                inst.save()

        self.stdout.write(self.style.SUCCESS('Демо-данные успешно созданы.'))
        self.stdout.write(f'  Пользователи: admin, storekeeper1, mechanic1 (пароль: {password})')
