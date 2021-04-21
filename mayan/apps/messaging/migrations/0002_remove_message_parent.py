from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='parent',
        ),
    ]
