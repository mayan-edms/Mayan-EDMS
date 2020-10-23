from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('converter', '0016_auto_20190814_0510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layertransformation',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Name'),
        ),
    ]
