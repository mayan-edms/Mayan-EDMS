from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0078_alter_documenttype_label')
    ]

    operations = [
        migrations.AddField(
            model_name='documentfile', name='size',
            field=models.PositiveIntegerField(
                blank=True, db_index=True, editable=False,
                help_text='The size of the file in bytes.', null=True,
                verbose_name='Size'
            )
        )
    ]
