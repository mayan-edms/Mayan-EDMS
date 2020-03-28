from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0026_auto_20150729_2140'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True,
                        primary_key=True
                    )
                ),
                ('comment', models.TextField(verbose_name='comment')),
                (
                    'submit_date', models.DateTimeField(
                        verbose_name='Date time submitted', db_index=True
                    )
                ),
                (
                    'document', models.ForeignKey(
                        on_delete=models.CASCADE, related_name='comments',
                        to='documents.Document', verbose_name='Document'
                    )
                ),
                (
                    'user', models.ForeignKey(
                        editable=False, on_delete=models.CASCADE,
                        related_name='comments', to=settings.AUTH_USER_MODEL,
                        verbose_name='User'
                    )
                ),
            ],
            options={
                'ordering': ('-submit_date',),
                'get_latest_by': 'submit_date',
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
            bases=(models.Model,),
        ),
    ]
