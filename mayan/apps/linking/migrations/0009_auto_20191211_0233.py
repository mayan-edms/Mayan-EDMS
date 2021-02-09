from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('linking', '0008_auto_20190429_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smartlink',
            name='dynamic_label',
            field=models.CharField(
                blank=True, help_text='Use this field to show a unique '
                'label depending on the document from which the smart '
                'link is being accessed.', max_length=96,
                verbose_name='Dynamic label'
            ),
        ),
        migrations.AlterField(
            model_name='smartlinkcondition',
            name='expression',
            field=models.TextField(
                help_text='The expression using document properties to '
                'be evaluated against the foreign document field.',
                verbose_name='Expression'
            ),
        ),
    ]
