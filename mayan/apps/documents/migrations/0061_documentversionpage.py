from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('documents', '0060_documentversion'),
    ]
    operations = [
        migrations.CreateModel(
            name='DocumentVersionPage',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'page_number', models.PositiveIntegerField(
                        blank=True, db_index=True, null=True,
                        verbose_name='Page number'
                    )
                ),
                ('object_id', models.PositiveIntegerField()),
                (
                    'content_type', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='contenttypes.ContentType'
                    )
                ),
                (
                    'document_version', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='pages', to='documents.DocumentVersion',
                        verbose_name='Document version'
                    )
                ),
            ],
            options={
                'verbose_name': 'Document version page',
                'verbose_name_plural': 'Document version pages',
                'ordering': ('page_number',),
                'unique_together': {('document_version', 'page_number')},
            },
        ),
    ]
