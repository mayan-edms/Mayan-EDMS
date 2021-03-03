from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0073_auto_20201130_0341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duplicateddocumentold',
            name='document',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='duplicates_old', to='documents.Document',
                verbose_name='Document'
            ),
        ),
    ]
