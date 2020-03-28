from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('converter', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transformation',
            old_name='transformation',
            new_name='name',
        ),
    ]
