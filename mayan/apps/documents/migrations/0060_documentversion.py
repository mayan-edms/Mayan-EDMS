from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0059_auto_20200918_0616'),
    ]
    operations = [
        migrations.CreateModel(
            name='DocumentVersion',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'timestamp', models.DateTimeField(
                        auto_now_add=True, db_index=True,
                        help_text='The server date and time when the '
                        'document version was created.',
                        verbose_name='Timestamp'
                    )
                ),
                (
                    'comment', models.TextField(
                        blank=True, default='',
                        help_text='An optional short text describing '
                        'the document version.', verbose_name='Comment'
                    )
                ),
                (
                    'document', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='versions', to='documents.Document',
                        verbose_name='Document'
                    )
                ),
            ],
            options={
                'verbose_name': 'Document version',
                'verbose_name_plural': 'Document versions',
                'ordering': ('timestamp',),
            },
        ),
    ]
