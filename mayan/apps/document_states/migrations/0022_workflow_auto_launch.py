from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('document_states', '0021_auto_20200624_0719'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflow',
            name='auto_launch',
            field=models.BooleanField(
                default=True, verbose_name='Launch workflow when document '
                'is created.'
            )
        )
    ]
