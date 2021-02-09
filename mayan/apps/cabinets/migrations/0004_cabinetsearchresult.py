from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('cabinets', '0003_auto_20200330_0851'),
    ]

    operations = [
        migrations.CreateModel(
            name='CabinetSearchResult',
            fields=[
            ],
            options={
                'verbose_name': 'Cabinet',
                'verbose_name_plural': 'Cabinets',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('cabinets.cabinet',),
        ),
    ]
