from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        (
            'document_states',
            '0026_alter_workflowtransitiontriggerevent_options'
        )
    ]

    operations = [
        migrations.AddField(
            model_name='workflowinstance', name='datetime',
            field=models.DateTimeField(
                auto_now_add=True, db_index=True,
                default=django.utils.timezone.now,
                help_text='Workflow instance creation date time.',
                verbose_name='Datetime'
            ), preserve_default=False
        )
    ]
