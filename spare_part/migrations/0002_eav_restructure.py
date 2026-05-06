from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spare_part', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SparePartTypeAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_required', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('attribute', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='spare_part.attribute',
                )),
                ('spare_part_type', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='type_attributes',
                    to='spare_part.spareparttype',
                )),
            ],
            options={
                'unique_together': {('spare_part_type', 'attribute')},
            },
        ),
        # Add nullable spare_part FK to AttributeValue
        migrations.AddField(
            model_name='attributevalue',
            name='spare_part',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='attribute_values',
                to='spare_part.sparepart',
            ),
        ),
        # Extend value field
        migrations.AlterField(
            model_name='attributevalue',
            name='value',
            field=models.CharField(max_length=255),
        ),
        # Remove old spare_part_type FK from AttributeValue
        migrations.RemoveField(
            model_name='attributevalue',
            name='spare_part_type',
        ),
        # Make spare_part non-nullable
        migrations.AlterField(
            model_name='attributevalue',
            name='spare_part',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='attribute_values',
                to='spare_part.sparepart',
            ),
        ),
        migrations.AlterUniqueTogether(
            name='attributevalue',
            unique_together={('spare_part', 'attribute')},
        ),
    ]
