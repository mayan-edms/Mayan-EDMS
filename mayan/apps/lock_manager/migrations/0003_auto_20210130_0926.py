from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('lock_manager', '0002_auto_20150604_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lock',
            name='name',
            field=models.CharField(
                max_length=255, unique=True, verbose_name='Name'
            ),
        ),
    ]
