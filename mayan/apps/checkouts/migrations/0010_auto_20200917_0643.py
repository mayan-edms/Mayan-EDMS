from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0058_auto_20200916_1146'),
        ('checkouts', '0009_rename_documentcheckout_field'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NewVersionBlock',
            new_name='NewFileBlock',
        ),
        migrations.AlterModelOptions(
            name='newfileblock',
            options={'verbose_name': 'New file block', 'verbose_name_plural': 'New file blocks'},
        ),
        migrations.AlterField(
            model_name='documentcheckout',
            name='block_new_file',
            field=models.BooleanField(default=True, help_text='Do not allow new file of this document to be uploaded.', verbose_name='Block new file upload'),
        ),
    ]
