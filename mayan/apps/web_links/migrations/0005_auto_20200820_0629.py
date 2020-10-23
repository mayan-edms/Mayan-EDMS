from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('web_links', '0004_make_labes_unique'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weblink',
            name='label',
            field=models.CharField(
                db_index=True, help_text='A short text describing the web '
                'link.', max_length=96, unique=True, verbose_name='Label'
            ),
        ),
    ]
