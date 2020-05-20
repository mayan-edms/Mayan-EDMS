from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('linking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResolvedSmartLink',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('linking.smartlink',),
        ),
    ]
