from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('metadata', '0009_auto_20180402_0339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metadatatype',
            name='default',
            field=models.CharField(
                blank=True,
                help_text="Enter a template to render. Use Django's default "
                "templating language "
                "(https://docs.djangoproject.com/en/1.11/ref/templates/builtins/)",
                max_length=128, null=True, verbose_name='Default'
            ),
        ),
        migrations.AlterField(
            model_name='metadatatype',
            name='lookup',
            field=models.TextField(
                blank=True,
                help_text="Enter a template to render. Must result in a comma "
                "delimited string. Use Django's default templating language "
                "(https://docs.djangoproject.com/en/1.11/ref/templates/builtins/).",
                null=True, verbose_name='Lookup'
            ),
        ),
    ]
