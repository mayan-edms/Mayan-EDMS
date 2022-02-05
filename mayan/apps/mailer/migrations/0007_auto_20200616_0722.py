from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('mailer', '0006_auto_20191213_0044')
    ]

    operations = [
        migrations.DeleteModel(name='LogEntry'),
        migrations.DeleteModel(name='UserMailerLogEntry')
    ]
