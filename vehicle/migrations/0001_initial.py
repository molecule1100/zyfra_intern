from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='VehicleType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_number', models.CharField(max_length=50)),
                ('brand', models.CharField(max_length=50)),
                ('date_purchase', models.DateField()),
                ('mileage', models.DecimalField(decimal_places=0, max_digits=7)),
                ('operation_status', models.CharField(
                    choices=[('1', 'В работе'), ('2', 'Простой'), ('3', 'Ремонт')],
                    max_length=50,
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('type', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to='vehicle.vehicletype',
                )),
            ],
        ),
        migrations.CreateModel(
            name='VehicleImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', sorl.thumbnail.fields.ImageField(upload_to='images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('vehicle', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='images',
                    to='vehicle.vehicle',
                )),
            ],
        ),
    ]
