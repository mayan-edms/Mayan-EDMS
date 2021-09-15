"""
Sort existing cabinets after adding:
    class MPTTMeta:
        order_insertion_by = ('label',)
"""
from django.db import migrations

from mptt.models import MPTTModel


def code_sort_existing_cabinets(apps, schema_editor):
    Cabinet = apps.get_model(app_label='cabinets', model_name='Cabinet')

    class ProxyCabinetWithTreeManager(MPTTModel, Cabinet):
        class MPTTMeta:
            order_insertion_by = ('label',)

        class Meta:
            proxy = True

    ProxyCabinetWithTreeManager.objects.rebuild()


class Migration(migrations.Migration):
    dependencies = [
        ('cabinets', '0004_cabinetsearchresult'),
    ]

    operations = [
        migrations.RunPython(
            code=code_sort_existing_cabinets,
            reverse_code=migrations.RunPython.noop
        ),
    ]
