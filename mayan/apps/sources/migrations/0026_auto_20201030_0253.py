from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sources', '0025_delete_sourcelog'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='backend_data',
            field=models.TextField(blank=True, verbose_name='Backend data'),
        ),
        migrations.AddField(
            model_name='source',
            name='backend_path',
            field=models.CharField(default='', help_text='The dotted Python path to the backend class.', max_length=128, verbose_name='Backend path'),
            preserve_default=False,
        ),
    ]
