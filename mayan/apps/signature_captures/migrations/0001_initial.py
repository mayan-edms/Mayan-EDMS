import re

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion

import mayan.apps.databases.model_mixins


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0080_populate_file_size')
    ]

    operations = [
        migrations.CreateModel(
            name='SignatureCapture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(blank=True, help_text='Data representing the handwritten signature.', verbose_name='Signature capture data')),
                ('svg', models.TextField(blank=True, help_text='Vector representation of the handwritten signature.', verbose_name='SVG signature capture data')),
                ('text', models.CharField(help_text='Print version of the captured signature.', max_length=224, verbose_name='Text')),
                ('date_time_created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Date and time created')),
                ('date_time_edited', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Date and time edited')),
                ('internal_name', models.CharField(db_index=True, help_text='This value will be used when referencing this signature capture in relationship to the document. Can only contain letters, numbers, and underscores.', max_length=255, validators=[django.core.validators.RegexValidator(re.compile('^[a-zA-Z0-9_]+\\Z'), "Enter a valid 'internal name' consisting of letters, numbers, and underscores.", 'invalid')], verbose_name='Internal name')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signature_captures', to='documents.document', verbose_name='Document')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signature_captures', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Signature capture',
                'verbose_name_plural': 'Signature captures',
                'ordering': ('-date_time_created',),
                'unique_together': {('document', 'internal_name')}
            },
            bases=(mayan.apps.databases.model_mixins.ExtraDataModelMixin, models.Model)
        )
    ]
