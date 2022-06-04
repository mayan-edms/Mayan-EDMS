from django.db import migrations, models
import django.db.models.deletion
import mayan.apps.databases.model_mixins


class Migration(migrations.Migration):
    dependencies = [
        ('document_states', '0027_workflowinstance_datetime')
    ]

    operations = [
        migrations.CreateModel(
            name='WorkflowStateEscalation',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'condition', models.TextField(
                        blank=True, help_text="The condition that will "
                        "determine if this object is executed or not. "
                        "Conditions that do not return any value, that "
                        "return the Python logical None, or an empty "
                        "string ('') are considered to be logical false, "
                        "any other value is considered to be the logical "
                        "true.", verbose_name='Condition'
                    )
                ),
                (
                    'priority', models.IntegerField(
                        blank=True, db_index=True, default=0,
                        help_text='Determine the order in which the '
                        'escalations will be evaluated. Escalations with '
                        'a lower priority number are executed before '
                        'escalations with a higher priority number.',
                        verbose_name='Priority'
                    )
                ),
                (
                    'enabled', models.BooleanField(
                        default=True, help_text='Enable automatic '
                        'transition the workflow after a specified '
                        'amount of time has elapsed in the state without '
                        'change.', verbose_name='Enabled'
                    )
                ),
                (
                    'unit', models.CharField(
                        blank=True, choices=[
                            ('days', 'Days'), ('hours', 'Hours'),
                            ('minutes', 'Minutes')
                        ], default='days', max_length=32,
                        verbose_name='Time unit'
                    )
                ),
                (
                    'amount', models.PositiveIntegerField(
                        blank=True, default=1, help_text='Amount of the '
                        'selected escalation units of time.',
                        verbose_name='Amount'
                    )
                ),
                (
                    'comment', models.TextField(
                        blank=True, help_text='Comment to save to the '
                        'workflow instance when the escalation is executed.',
                        verbose_name='Comment'
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
            },
            bases=(
                mayan.apps.databases.model_mixins.ExtraDataModelMixin,
                models.Model
            )
        )
    ]
