from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('tags', '0002_tag_selection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='color',
        ),
    ]
