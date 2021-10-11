from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0076_auto_20210908_0837'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteDocumentProxy',
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
