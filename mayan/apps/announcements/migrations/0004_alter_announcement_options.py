from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('announcements', '0003_auto_20210414_2323')
    ]

    operations = [
        migrations.AlterModelOptions(
            name='announcement',
            options={
                'ordering': ('label',), 'verbose_name': 'Announcement',
                'verbose_name_plural': 'Announcements'
            }
        )
    ]
