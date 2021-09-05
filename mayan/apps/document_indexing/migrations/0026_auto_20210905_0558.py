from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('document_indexing', '0025_auto_20210822_0052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indextemplatenode',
            name='expression',
            field=models.TextField(
                help_text="Enter a template to render. Use Django's "
                "default templating language.",
                verbose_name='Indexing expression'
            ),
        ),
    ]
