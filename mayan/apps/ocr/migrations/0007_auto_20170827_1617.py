from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0006_auto_20170823_0553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentpageocrcontent',
            name='document_page',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='ocr_content', to='documents.DocumentPage',
                verbose_name='Document page'
            ),
        ),
    ]
