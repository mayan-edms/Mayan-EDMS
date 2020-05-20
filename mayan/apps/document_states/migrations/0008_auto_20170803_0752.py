from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('document_states', '0007_auto_20170803_0728'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workflowtransition',
            name='trigger_time_period',
        ),
        migrations.RemoveField(
            model_name='workflowtransition',
            name='trigger_time_unit',
        ),
    ]
