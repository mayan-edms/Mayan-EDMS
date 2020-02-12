import re

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def operation_update_event_types_names(apps, schema_editor):
    Action = apps.get_model(app_label='actstream', model_name='Action')
    StoredEventType = apps.get_model(
        app_label='events', model_name='StoredEventType'
    )

    known_namespaces = {
        'documents_': 'documents.',
        'checkouts_': 'checkouts.',
        'document_comment_': 'document_comments.',
        'parsing_document_': 'document_parsing.',
        'ocr_': 'ocr.',
        'tag_': 'tags.',
    }

    pattern = re.compile('|'.join(known_namespaces.keys()))

    for event_type in StoredEventType.objects.using(schema_editor.connection.alias).all():
        event_type.name = pattern.sub(
            lambda x: known_namespaces[x.group()], event_type.name
        )
        event_type.save()

    for action in Action.objects.using(schema_editor.connection.alias).all():
        action.verb = pattern.sub(
            lambda x: known_namespaces[x.group()], action.verb
        )
        action.save()


def operation_revert_event_types_names(apps, schema_editor):
    Action = apps.get_model(app_label='actstream', model_name='Action')
    StoredEventType = apps.get_model(
        app_label='events', model_name='StoredEventType'
    )

    known_namespaces = {
        r'documents\.': 'documents_',
        r'checkouts\.': 'checkouts_',
        r'document_comments\.': 'document_comment_',
        r'document_parsing\.': 'parsing_document_',
        r'ocr\.': 'ocr_',
        r'tags\.': 'tag_',
    }

    pattern = re.compile('|'.join(known_namespaces.keys()))

    for event_type in StoredEventType.objects.using(schema_editor.connection.alias).all():
        old_name = event_type.name
        new_name = pattern.sub(
            lambda x: known_namespaces[x.group().replace('.', '\\.')],
            event_type.name
        )
        event_type.name = new_name
        if old_name == new_name:
            event_type.delete()
        else:
            event_type.save()

    for action in Action.objects.using(schema_editor.connection.alias).all():
        new_name = pattern.sub(
            lambda x: known_namespaces[x.group().replace('.', '\\.')],
            action.verb
        )
        action.verb = new_name
        action.save()


class Migration(migrations.Migration):

    replaces = [('events', '0001_initial'), ('events', '0002_eventsubscription'), ('events', '0003_notification'), ('events', '0004_auto_20170731_0423'), ('events', '0005_auto_20170731_0452'), ('events', '0006_objecteventsubscription'), ('events', '0007_auto_20170802_0823'), ('events', '0008_auto_20180315_0029')]

    dependencies = [
        ('actstream', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('actstream', '0002_remove_action_data'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StoredEventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Stored event type',
                'verbose_name_plural': 'Stored event types',
            },
        ),
        migrations.CreateModel(
            name='EventSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_subscriptions', to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('stored_event_type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='event_subscriptions', to='events.StoredEventType', verbose_name='Event type')),
            ],
            options={
                'verbose_name': 'Event subscription',
                'verbose_name_plural': 'Event subscriptions',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False, verbose_name='Read')),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='actstream.Action', verbose_name='Action')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
        migrations.RunPython(
            code=operation_update_event_types_names,
            reverse_code=operation_revert_event_types_names,
        ),
        migrations.CreateModel(
            name='ObjectEventSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('stored_event_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='object_subscriptions', to='events.StoredEventType', verbose_name='Event type')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='object_subscriptions', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Object event subscription',
                'verbose_name_plural': 'Object event subscriptions',
            },
        ),
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ('-action__timestamp',), 'verbose_name': 'Notification', 'verbose_name_plural': 'Notifications'},
        ),
        migrations.AlterField(
            model_name='eventsubscription',
            name='stored_event_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_subscriptions', to='events.StoredEventType', verbose_name='Event type'),
        ),
    ]
