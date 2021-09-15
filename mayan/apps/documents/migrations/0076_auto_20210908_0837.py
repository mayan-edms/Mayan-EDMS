from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0075_delete_duplicateddocumentold'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecentlyAccessedDocumentProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Recently accessed document',
                'verbose_name_plural': 'Recently accessed documents',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('documents.document',),
        ),
        migrations.AlterField(
            model_name='document',
            name='datetime_created',
            field=models.DateTimeField(
                auto_now_add=True, db_index=True, help_text='The date and '
                'time of the document creation.', verbose_name='Created'
            ),
        ),
    ]
