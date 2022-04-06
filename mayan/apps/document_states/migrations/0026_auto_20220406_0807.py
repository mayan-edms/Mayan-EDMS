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
        migrations.AlterModelOptions(
            name='workflowtransitiontriggerevent',
            options={
                'ordering': ('event_type__name',),
                'verbose_name': 'Workflow transition trigger event',
                'verbose_name_plural': 'Workflow transitions trigger events'
            }
        ),
        migrations.AddField(
            model_name='workflowinstance',
            name='datetime',
            field=models.DateTimeField(
                auto_now_add=True, db_index=True,
                default=django.utils.timezone.now,
                help_text='Workflow instance creation date time.',
                verbose_name='Datetime'
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='WorkflowStateEscalation',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True,
                        serialize=False, verbose_name='ID'
                    )
                ),
                (
                    'priority', models.IntegerField(
                        blank=True, db_index=True, default=0,
                        help_text='Determine the order in which the escalations will be evaluated.', verbose_name='Priority'
                    )
                ),
                (
                    'enabled', models.BooleanField(
                        default=True, help_text='Enable automatic transition the workflow after a specified amount of time has elapsed in the state without change.', verbose_name='Enable escalation'
                    )
                ),
                (
                    'unit', models.CharField(
                        blank=True, choices=[
                            ('days', 'Days'), ('hours', 'Hours'),
                            ('minutes', 'Minutes')
                        ], default='days', max_length=32,
                        verbose_name='Expiration time unit'
                    )
                ),
                (
                    'amount', models.PositiveIntegerField(
                        blank=True, default=1, help_text='Amount of the selected expiration units of time.', verbose_name='Expiration amount'
                    )
                ),
                (
                    'condition', models.TextField(
                        blank=True, help_text="The condition that will determine if this state escalation is executed or not. The condition is evaluated against the workflow instance. Conditions that do not return any value, that return the Python logical None, or an empty string ('') are considered to be logical false, any other value is considered to be the logical true.", verbose_name='Condition'
                    )
                ),
                (
                    'state', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='escalations',
                        to='document_states.workflowstate',
                        verbose_name='Workflow state'
                    )
                ),
                (
                    'transition', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='escalations',
                        to='document_states.workflowtransition',
                        verbose_name='Transition'
                    )
                )
            ],
            options={
                'verbose_name': 'Workflow state escalation',
                'verbose_name_plural': 'Workflow state escalations',
                'ordering': ('priority',),
                'unique_together': {('state', 'transition')},
            }
        )
    ]
