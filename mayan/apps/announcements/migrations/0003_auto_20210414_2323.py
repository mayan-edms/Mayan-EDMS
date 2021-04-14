from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('announcements', '0002_auto_20210212_1022'),
    ]

    operations = [
        migrations.AlterField(
            field=models.TextField(
                help_text='The actual text to be displayed.',
                verbose_name='Text'
            ), model_name='announcement', name='text'
        ),
    ]
