from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


GROUPS = {
    'Администраторы': {
        'vehicle': ['vehicletype', 'vehicle', 'vehicleimage'],
        'spare_part': ['spareparttype', 'sparepart', 'spartepartimage', 'attribute', 'attributevalue',
                       'spareparttypeattribute', 'sparepartinstallation'],
        'all_perms': True,
    },
    'Кладовщики': {
        'spare_part_crud': ['spareparttype', 'sparepart', 'attribute', 'attributevalue', 'spareparttypeattribute'],
        'vehicle_view': ['vehicle', 'vehicletype'],
    },
    'Механики': {
        'vehicle_crud': ['vehicle', 'vehicletype'],
        'spare_part_view': ['sparepart', 'spareparttype'],
        'installation': ['sparepartinstallation'],
    },
}


def setup_groups():
    admins, _ = Group.objects.get_or_create(name='Администраторы')
    storekeeper, _ = Group.objects.get_or_create(name='Кладовщики')
    mechanic, _ = Group.objects.get_or_create(name='Механики')

    admins.permissions.set(Permission.objects.all())

    spare_part_models = ['spareparttype', 'sparepart', 'attribute', 'attributevalue',
                         'spareparttypeattribute', 'sparepartinstallation']
    vehicle_models = ['vehicle', 'vehicletype', 'vehicleimage']

    sk_perms = []
    for model in spare_part_models:
        try:
            ct = ContentType.objects.get(app_label='spare_part', model=model)
            sk_perms += list(Permission.objects.filter(content_type=ct))
        except ContentType.DoesNotExist:
            pass
    for model in vehicle_models:
        try:
            ct = ContentType.objects.get(app_label='vehicle', model=model)
            sk_perms += list(Permission.objects.filter(content_type=ct, codename__startswith='view_'))
        except ContentType.DoesNotExist:
            pass
    storekeeper.permissions.set(sk_perms)

    mech_perms = []
    for model in vehicle_models:
        try:
            ct = ContentType.objects.get(app_label='vehicle', model=model)
            mech_perms += list(Permission.objects.filter(content_type=ct))
        except ContentType.DoesNotExist:
            pass
    for model in ['sparepart', 'spareparttype', 'sparepartinstallation']:
        try:
            ct = ContentType.objects.get(app_label='spare_part', model=model)
            if model == 'sparepartinstallation':
                mech_perms += list(Permission.objects.filter(content_type=ct))
            else:
                mech_perms += list(Permission.objects.filter(content_type=ct, codename__startswith='view_'))
        except ContentType.DoesNotExist:
            pass
    mechanic.permissions.set(mech_perms)


class Command(BaseCommand):
    help = 'Создать группы пользователей: Администраторы, Кладовщики, Механики'

    def handle(self, *args, **options):
        setup_groups()
        self.stdout.write(self.style.SUCCESS('Группы успешно созданы.'))
