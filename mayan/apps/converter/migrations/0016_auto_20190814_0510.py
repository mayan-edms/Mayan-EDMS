from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('converter', '0015_auto_20190814_0014'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='transformation',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='transformation',
            name='content_type',
        ),
        migrations.DeleteModel(
            name='Transformation',
        ),
    ]
