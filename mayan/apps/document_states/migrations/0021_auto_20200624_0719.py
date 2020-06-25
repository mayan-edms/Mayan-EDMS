from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_states', '0020_auto_20200311_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workflowstateaction',
            name='condition',
            field=models.TextField(blank=True, help_text="The condition that will determine if this state action is executed or not. The condition is evaluated against the workflow instance. Conditions that do not return any value, that return the Python logical None, or an empty string ('') are considered to be logical false, any other value is considered to be the logical true.", verbose_name='Condition'),
        ),
        migrations.AlterField(
            model_name='workflowtransition',
            name='condition',
            field=models.TextField(blank=True, help_text="The condition that will determine if this transition is enabled or not. The condition is evaluated against the workflow instance. Conditions that do not return any value, that return the Python logical None, or an empty string ('') are considered to be logical false, any other value is considered to be the logical true.", verbose_name='Condition'),
        ),
    ]
