from django.contrib.auth import get_user_model

from mayan.apps.common.classes import QuerysetParametersSerializer
from mayan.celery import app

from .classes import ActionExporter


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
