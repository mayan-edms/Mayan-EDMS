from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0005_auto_20150617_0358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentpage',
            name='content_old',
        ),
    ]
