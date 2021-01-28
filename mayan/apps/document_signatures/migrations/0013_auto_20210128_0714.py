from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('document_signatures', '0012_auto_20200917_0605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signaturebasemodel',
            name='date',
        ),
        migrations.AddField(
            model_name='signaturebasemodel',
            name='date_time',
            field=models.DateTimeField(
                blank=True, editable=False, null=True,
                verbose_name='Date and time signed'
            ),
        ),
    ]
