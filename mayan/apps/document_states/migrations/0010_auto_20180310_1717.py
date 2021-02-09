from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('document_states', '0009_auto_20170807_0612'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workflowinstancelogentry',
            options={
                'ordering': ('datetime',),
                'verbose_name': 'Workflow instance log entry',
                'verbose_name_plural': 'Workflow instance log entries'
            },
        ),
    ]
