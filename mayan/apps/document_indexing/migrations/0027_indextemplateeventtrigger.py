from django.db import migrations, models
import django.db.models.deletion

import mayan.apps.databases.model_mixins


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0008_auto_20180315_0029'),
        ('document_indexing', '0026_alter_indexinstancenode_options')
    ]

    operations = [
        migrations.CreateModel(
            name='IndexTemplateEventTrigger',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True,
                        serialize=False, verbose_name='ID'
                    )
                ),
                (
                    'index_template', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='event_triggers',
                        to='document_indexing.indextemplate',
                        verbose_name='Index template'
                    )
                ),
                (
                    'stored_event_type', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='events.storedeventtype',
                        verbose_name='Event type'
                    )
                )
            ],
            options={
                'verbose_name': 'Index template event trigger',
                'verbose_name_plural': 'Index template event triggers',
                'unique_together': {('index_template', 'stored_event_type')},
            },
            bases=(
                mayan.apps.databases.model_mixins.ExtraDataModelMixin,
                models.Model
            )
        )
    ]
