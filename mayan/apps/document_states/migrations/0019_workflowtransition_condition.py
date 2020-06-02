from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('document_states', '0018_auto_20200129_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflowtransition',
            name='condition',
            field=models.TextField(
                blank=True, help_text="The condition that will "
                "determine if this transition is enabled or not. "
                "The condition is evaluated against the workflow "
                "instance. Condition that return None or an empty "
                "string ('') are considered to be logical false, any "
                "other value is considered to be the logical true.",
                verbose_name='Condition'
            ),
        ),
    ]
