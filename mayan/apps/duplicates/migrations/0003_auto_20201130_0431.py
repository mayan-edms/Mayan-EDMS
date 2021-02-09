from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('duplicates', '0002_auto_20201130_0342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duplicateddocument',
            name='document',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='duplicates', to='documents.Document',
                verbose_name='Document'
            ),
        ),
    ]
