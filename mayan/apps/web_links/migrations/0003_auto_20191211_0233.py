from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('web_links', '0002_auto_20191210_0436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weblink',
            name='template',
            field=models.TextField(
                help_text='Template that will be used to craft the '
                'final URL of the web link.', verbose_name='Template'
            ),
        ),
    ]
