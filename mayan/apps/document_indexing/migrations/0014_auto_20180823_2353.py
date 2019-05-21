from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_indexing', '0013_auto_20170714_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indextemplatenode',
            name='expression',
            field=models.TextField(
                help_text="Enter a template to render. Use Django's default "
                "templating language "
                "(https://docs.djangoproject.com/en/1.11/ref/templates/builtins/)",
                verbose_name='Indexing expression'
            ),
        ),
    ]
