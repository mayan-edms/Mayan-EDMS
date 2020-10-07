from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('document_states', '0022_workflow_auto_launch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workflow',
            name='auto_launch',
            field=models.BooleanField(
                default=True, help_text='Launch workflow when document is '
                'created.', verbose_name='Auto launch'
            ),
        ),
    ]
