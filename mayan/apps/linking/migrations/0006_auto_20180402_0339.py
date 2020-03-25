from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('linking', '0005_auto_20150729_2344'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='smartlink',
            options={
                'ordering': ('label',), 'verbose_name': 'Smart link',
                'verbose_name_plural': 'Smart links'
            },
        ),
        migrations.AlterField(
            model_name='smartlink',
            name='label',
            field=models.CharField(
                db_index=True, max_length=96, verbose_name='Label'
            ),
        ),
    ]
