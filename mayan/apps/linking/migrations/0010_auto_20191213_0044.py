from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('linking', '0009_auto_20191211_0233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smartlink',
            name='label',
            field=models.CharField(
                db_index=True, help_text='A short text describing the '
                'smart link.', max_length=128, verbose_name='Label'
            ),
        ),
    ]
