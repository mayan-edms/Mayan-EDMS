from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0036_auto_20161222_0534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='language',
            field=models.CharField(
                blank=True, default='eng', max_length=8,
                verbose_name='Language'
            ),
        ),
    ]
