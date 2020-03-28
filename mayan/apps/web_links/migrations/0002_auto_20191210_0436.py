from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('web_links', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weblink',
            name='label',
            field=models.CharField(
                db_index=True, help_text='A short text describing the '
                'web link.', max_length=96, verbose_name='Label'
            ),
        ),
        migrations.AlterField(
            model_name='weblink',
            name='template',
            field=models.TextField(
                help_text='Template that will be used to craft the '
                'final URL of the web link. The {{ document }} variable '
                'is available to the template.', verbose_name='Template'
            ),
        ),
    ]
