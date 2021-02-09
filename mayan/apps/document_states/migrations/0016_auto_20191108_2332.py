from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('document_states', '0015_auto_20190701_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workflowstate',
            name='completion',
            field=models.IntegerField(
                blank=True, default=0,
                help_text='The percent of completion that this state '
                'represents in relation to the workflow. Use numbers '
                'without the percent sign.', verbose_name='Completion'
            ),
        ),
        migrations.AlterField(
            model_name='workflowstate',
            name='initial',
            field=models.BooleanField(
                default=False, help_text='The state at which the '
                'workflow will start in. Only one state can be the '
                'initial state.', verbose_name='Initial'
            ),
        ),
        migrations.AlterField(
            model_name='workflowstateaction',
            name='when',
            field=models.PositiveIntegerField(
                choices=[
                    (1, 'On entry'), (2, 'On exit')
                ], default=1,
                help_text='At which moment of the state this action '
                'will execute.', verbose_name='When'
            ),
        ),
    ]
