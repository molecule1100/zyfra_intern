from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spare_part', '0002_eav_restructure'),
        ('vehicle', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SparePartInstallation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installed_at', models.DateTimeField(auto_now_add=True)),
                ('uninstalled_at', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('spare_part', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='installations',
                    to='spare_part.sparepart',
                )),
                ('vehicle', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='installations',
                    to='vehicle.vehicle',
                )),
                ('installed_by', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='installations_made',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('uninstalled_by', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='uninstallations_made',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'ordering': ['-installed_at'],
            },
        ),
    ]
