from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0053_auto_20200129_0926'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrashedDocument',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('documents.document',),
        ),
    ]
