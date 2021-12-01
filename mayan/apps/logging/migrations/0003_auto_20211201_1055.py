from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('logging', '0002_auto_20211201_1055')
    ]

    operations = [
        migrations.AlterField(
            model_name='storederrorlog',
            name='name',
            field=models.CharField(
                max_length=128, unique=True, verbose_name='Internal name'
            )
        )
    ]
