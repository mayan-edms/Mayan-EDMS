from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0077_favoritedocumentproxy'),
        ('checkouts', '0011_delete_newfileblock')
    ]

    operations = [
        migrations.AlterField(
            model_name='documentcheckout',
            name='document',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='checkout', to='documents.document',
                verbose_name='Document'
            )
        )
    ]
