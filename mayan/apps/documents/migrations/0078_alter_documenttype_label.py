from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0077_favoritedocumentproxy')
    ]

    operations = [
        migrations.AlterField(
            model_name='documenttype',
            name='label',
            field=models.CharField(
                help_text='A short text identifying the document type.',
                max_length=196, unique=True, verbose_name='Label'
            )
        )
    ]
