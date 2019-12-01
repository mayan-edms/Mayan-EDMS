from __future__ import unicode_literals

from django.db import migrations, models
import mayan.apps.document_signatures.models
import mayan.apps.storage.classes


class Migration(migrations.Migration):

    dependencies = [
        ('document_signatures', '0009_auto_20190711_0544'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='signaturebasemodel',
            options={
                'ordering': ('pk',),
                'verbose_name': 'Document version signature',
                'verbose_name_plural': 'Document version signatures'
            },
        ),
        migrations.AlterField(
            model_name='detachedsignature',
            name='signature_file',
            field=models.FileField(
                blank=True, help_text='Signature file previously generated.',
                null=True,
                storage=mayan.apps.storage.classes.FakeStorageSubclass(),
                upload_to=mayan.apps.document_signatures.models.upload_to,
                verbose_name='Signature file'
            ),
        ),
        migrations.AlterField(
            model_name='signaturebasemodel',
            name='key_id',
            field=models.CharField(
                help_text='ID of the key that will be used to sign the '
                'document.', max_length=40, verbose_name='Key ID'
            ),
        ),
    ]
