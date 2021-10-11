from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from mayan.apps.common.classes import QuerysetParametersSerializer
from mayan.celery import app

from .classes import ActionExporter
from .events import event_events_cleared
from .permissions import permission_events_clear


@app.task(ignore_result=True)
def task_event_queryset_clear(
    decomposed_queryset, target_content_type_id=None, target_object_id=None,
    user_id=None
):
    AccessControlList = apps.get_model(
        app_label='acls', model_name='AccessControlList'
    )

    queryset = QuerysetParametersSerializer.rebuild(
        decomposed_queryset=decomposed_queryset
    )

    if user_id:
        user = get_user_model().objects.get(pk=user_id)
    else:
        user = None

    if target_content_type_id:
        target_content_type = ContentType.objects.get(
            pk=target_content_type_id
        )
        target = target_content_type.get_object_for_this_type(
            pk=target_object_id
        )
    else:
        target = user

    AccessControlList = apps.get_model(
        app_label='acls', model_name='AccessControlList'
    )

    if user:
        queryset = AccessControlList.objects.restrict_queryset(
            queryset=queryset,
            permission=permission_events_clear,
            user=user
        )

    commit_event = queryset.exists()

    queryset.delete()

    if commit_event:
        event_events_cleared.commit(actor=user, target=target)


@app.task(ignore_result=True)
def task_event_queryset_export(decomposed_queryset, user_id=None):
    queryset = QuerysetParametersSerializer.rebuild(
        decomposed_queryset=decomposed_queryset
    )

    if user_id:
        user = get_user_model().objects.get(pk=user_id)
    else:
        user = None

    ActionExporter(queryset=queryset).export_to_download_file(user=user)
