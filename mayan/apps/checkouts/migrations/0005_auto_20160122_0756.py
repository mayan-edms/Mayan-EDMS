from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkouts', '0004_auto_20150617_0330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentcheckout',
            name='document',
            field=models.OneToOneField(
                on_delete=models.CASCADE, to='documents.Document',
                verbose_name='Document'
            ),
        ),
    ]
