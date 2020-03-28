import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0040_auto_20170725_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
