from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('tags', '0003_remove_tag_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='selection',
            new_name='color',
        ),
    ]
