from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0039_duplicateddocument'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentversion',
            options={
                'ordering': ('timestamp',),
                'verbose_name': 'Document version',
                'verbose_name_plural': 'Document version'
            },
        ),
    ]
