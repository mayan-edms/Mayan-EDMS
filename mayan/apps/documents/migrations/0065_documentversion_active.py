from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0064_auto_20201012_0544'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentversion',
            name='active',
            field=models.BooleanField(
                default=True, help_text='Determines the active version '
                'of the document.', verbose_name='Active'
            ),
        ),
    ]
