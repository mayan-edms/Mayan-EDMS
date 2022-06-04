from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('tags', '0008_auto_20180917_0646')
    ]

    operations = [
        migrations.AlterField(
            model_name='tag', name='color', field=models.CharField(
                help_text='The RGB color values for the tag.', max_length=7,
                verbose_name='Color'
            )
        )
    ]
