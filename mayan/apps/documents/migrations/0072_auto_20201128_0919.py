from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0071_auto_20201128_0330'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecentlyCreatedDocument',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('documents.document',),
        ),
        migrations.AlterModelOptions(
            name='favoritedocument',
            options={
                'ordering': ('datetime_added',),
                'verbose_name': 'Favorite document',
                'verbose_name_plural': 'Favorite documents'
            },
        ),
        migrations.AddField(
            model_name='favoritedocument',
            name='datetime_added',
            field=models.DateTimeField(
                auto_now=True, db_index=True,
                verbose_name='Date and time added'
            ),
        ),
        migrations.AlterField(
            model_name='document',
            name='datetime_created',
            field=models.DateTimeField(
                auto_now_add=True, db_index=True,
                help_text='The server date and time when the document '
                'was finally processed and created in the system.',
                verbose_name='Created'
            ),
        ),
    ]
