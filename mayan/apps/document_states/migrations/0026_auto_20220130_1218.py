from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        (
            'document_states',
            '0025_alter_workflowtransitiontriggerevent_unique_together'
        )
    ]

    operations = [
        migrations.AddField(
            model_name='workflowinstance',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, db_index=True, default=django.utils.timezone.now, help_text='Workflow instance creation date time.', verbose_name='Datetime'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workflowstate',
            name='expiration_amount',
            field=models.PositiveIntegerField(blank=True, default=1, help_text='Amount of the selected expiration units of time.', verbose_name='Expiration amount'),
        ),
        migrations.AddField(
            model_name='workflowstate',
            name='expiration_enabled',
            field=models.BooleanField(default=False, help_text='Enable automatic transition the workflow after a specified amount of time has elapsed in the state without change.', verbose_name='Enable expiration'),
        ),
        migrations.AddField(
            model_name='workflowstate',
            name='expiration_transition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='states', to='document_states.workflowtransition', verbose_name='Expiration transition'),
        ),
        migrations.AddField(
            model_name='workflowstate',
            name='expiration_unit',
            field=models.CharField(blank=True, choices=[('days', 'Days'), ('hours', 'Hours'), ('minutes', 'Minutes')], default='days', max_length=32, verbose_name='Expiration time unit'),
        ),
    ]
