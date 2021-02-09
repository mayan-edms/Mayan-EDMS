from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('django_gpg', '0006_auto_20160510_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='key',
            name='creation_date',
            field=models.DateTimeField(
                editable=False, verbose_name='Creation date'
            ),
        ),
        migrations.AlterField(
            model_name='key',
            name='expiration_date',
            field=models.DateTimeField(
                blank=True, editable=False, null=True,
                verbose_name='Expiration date'
            ),
        ),
    ]
