from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('document_comments', '0005_auto_20210130_0658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(verbose_name='Text'),
        ),
    ]
