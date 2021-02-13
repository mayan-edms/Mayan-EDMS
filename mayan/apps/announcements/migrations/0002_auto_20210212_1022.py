from django.db import migrations


def code_copy_messages(apps, schema_editor):
    AccessControlList = apps.get_model(
        app_label='acls', model_name='AccessControlList'
    )
    Action = apps.get_model(
        app_label='actstream', model_name='Action'
    )
    Announcement = apps.get_model(
        app_label='announcements', model_name='Announcement'
    )
    ContentType = apps.get_model(
        app_label='contenttypes', model_name='ContentType'
    )
    Message = apps.get_model(app_label='motd', model_name='Message')
    StoredEventType = apps.get_model(
        app_label='events', model_name='StoredEventType'
    )
    StoredPermission = apps.get_model(
        app_label='permissions', model_name='StoredPermission'
    )

    announcement_content_type = ContentType.objects.get_for_model(
        model=Announcement
    )
    message_content_type = ContentType.objects.get_for_model(model=Message)

    # Copy the messages.
    for message in Message.objects.using(alias=schema_editor.connection.alias).all():
        announcement = Announcement.objects.create(
            enabled=message.enabled, label=message.label,
            text=message.message, start_datetime=message.start_datetime,
            end_datetime=message.end_datetime
        )

        message_acls_queryset = AccessControlList.objects.using(
            alias=schema_editor.connection.alias
        ).filter(
            content_type=message_content_type, object_id=message.pk
        )

        # Copy the ACLs.
        for message_acls in message_acls_queryset:
            announcement_acl = AccessControlList.objects.create(
                content_type=announcement_content_type, object_id=announcement.pk,
                role=message_acls.role
            )
            announcement_acl.permissions.set(message_acls.permissions.all())

        message_action_queryset = Action.objects.using(
            alias=schema_editor.connection.alias
        ).filter(
            target_content_type=message_content_type,
            target_object_id=message.pk
        )

        # Copy the actions.
        for message_action in message_action_queryset:
            Action.objects.create(
                actor_content_type=message_action.actor_content_type,
                actor_object_id=message_action.actor_object_id,
                description=message_action.description,
                target_content_type=announcement_content_type,
                target_object_id=announcement.pk,
                action_object_content_type=message_action.action_object_content_type,
                action_object_object_id=message_action.action_object_object_id,
                timestamp=message_action.timestamp,
                public=message_action.public,
                verb=message_action.verb
            )

        stored_event_queryset = StoredEventType.objects.using(
            alias=schema_editor.connection.alias
        ).filter(name__startswith='motd')

        # Update the stored events of the MOTD app.
        for stored_event_type in stored_event_queryset:
            stored_event_type.name.replace('motd', 'announcements').replace('message', 'announcement')
            stored_event_type.save()

        stored_permission_queryset = StoredPermission.objects.using(
            alias=schema_editor.connection.alias
        ).filter(namespace='motd')

        # Update the stored permissions of the MOTD app.
        for stored_permission in stored_permission_queryset:
            stored_permission.namespace.replace('motd', 'announcements')
            stored_permission.name.replace('message', 'announcement')
            stored_permission.save()


def reverse_code_copy_messages(apps, schema_editor):
    AccessControlList = apps.get_model(
        app_label='acls', model_name='AccessControlList'
    )
    Action = apps.get_model(
        app_label='actstream', model_name='Action'
    )
    Announcement = apps.get_model(
        app_label='announcements', model_name='Announcement'
    )
    ContentType = apps.get_model(
        app_label='contenttypes', model_name='ContentType'
    )
    Message = apps.get_model(app_label='motd', model_name='Message')
    StoredEventType = apps.get_model(
        app_label='events', model_name='StoredEventType'
    )
    StoredPermission = apps.get_model(
        app_label='permissions', model_name='StoredPermission'
    )

    announcement_content_type = ContentType.objects.get_for_model(
        model=Announcement
    )

    message_content_type = ContentType.objects.get_for_model(model=Message)

    # Copy the announcements.
    for announcement in Announcement.objects.using(alias=schema_editor.connection.alias).all():
        message = Message.objects.create(
            enabled=announcement.enabled, label=announcement.label,
            message=announcement.text,
            start_datetime=announcement.start_datetime,
            end_datetime=announcement.end_datetime
        )

        announcement_acls_queryset = AccessControlList.objects.using(
            alias=schema_editor.connection.alias
        ).filter(
            content_type=announcement_content_type, object_id=announcement.pk
        )

        # Copy the ACLs.
        for announcement_acls in announcement_acls_queryset.all():
            message_acl = AccessControlList.objects.create(
                content_type=message_content_type, object_id=message.pk,
                role=announcement_acls.role
            )
            message_acl.permissions.set(announcement_acls.permissions.all())

        announcement_action_queryset = Action.objects.using(
            alias=schema_editor.connection.alias
        ).filter(
            target_content_type=announcement_content_type,
            target_object_id=announcement.pk
        )

        # Update the stored events of the announcements app.
        for announcement_action in announcement_action_queryset.all():
            Action.objects.create(
                actor_content_type=announcement_action.actor_content_type,
                actor_object_id=announcement_action.actor_object_id,
                description=announcement_action.description,
                target_content_type=message_content_type,
                target_object_id=message.pk,
                action_object_content_type=announcement_action.action_object_content_type,
                action_object_object_id=announcement_action.action_object_object_id,
                timestamp=announcement_action.timestamp,
                public=announcement_action.public,
                verb=announcement_action.verb
            )

        stored_event_queryset = StoredEventType.objects.using(
            alias=schema_editor.connection.alias
        ).filter(name__startswith='motd')

        # Update the stored events of the announcements app.
        for stored_event_type in stored_event_queryset:
            stored_event_type.name.replace('announcements', 'motd').replace('announcement', 'message')
            stored_event_type.save()

        stored_permission_queryset = StoredPermission.objects.using(
            alias=schema_editor.connection.alias
        ).filter(namespace='announcements')

        # Update the stored permissions of the announcements app.
        for stored_permission in stored_permission_queryset:
            stored_permission.namespace.replace('announcements', 'motd')
            stored_permission.name.replace('announcement', 'message')
            stored_permission.save()


class Migration(migrations.Migration):
    dependencies = [
        ('acls', '0004_auto_20210130_0322'),
        ('announcements', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('events', '0008_auto_20180315_0029'),
        ('permissions', '0004_auto_20191213_0044'),
    ]

    operations = [
        migrations.RunPython(
            code=code_copy_messages,
            reverse_code=reverse_code_copy_messages
        ),
    ]
