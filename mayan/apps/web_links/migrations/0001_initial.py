from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('documents', '0050_auto_20190725_0451'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebLink',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'label', models.CharField(
                        db_index=True, help_text='A short text describing '
                        'the weblink.', max_length=96, verbose_name='Label'
                    )
                ),
                (
                    'template', models.TextField(
                        help_text='Template that will be used to craft the '
                        'final URL of the weblink. The {{ document }} '
                        'variable is available to the template.',
                        verbose_name='Template'
                    )
                ),
                (
                    'enabled', models.BooleanField(
                        default=True, verbose_name='Enabled'
                    )
                ),
                (
                    'document_types', models.ManyToManyField(
                        related_name='web_links',
                        to='documents.DocumentType',
                        verbose_name='Document types'
                    )
                ),
            ],
            options={
                'ordering': ('label',),
                'verbose_name': 'Web link',
                'verbose_name_plural': 'Web links',
            },
        ),
        migrations.CreateModel(
            name='ResolvedWebLink',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('web_links.weblink',),
        ),
    ]
