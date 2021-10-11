from django.apps import apps
from django.contrib.auth import get_user_model

from mayan.celery import app


@app.task(ignore_result=True)
def task_send_object(
    content_type_id, body, object_id, sender, subject, recipient,
    user_mailer_id, as_attachment=False,
    content_function_dotted_path=None,
    mime_type_function_dotted_path=None,
    object_name=None, organization_installation_url=None, user_id=None
):
    ContentType = apps.get_model(
        app_label='contenttypes', model_name='ContentType'
    )
    UserMailer = apps.get_model(
        app_label='mailer', model_name='UserMailer'
    )
    User = get_user_model()

    content_type = ContentType.objects.get(pk=content_type_id)
    obj = content_type.get_object_for_this_type(pk=object_id)

    user_mailer = UserMailer.objects.get(pk=user_mailer_id)

    if user_id:
        user = User.objects.get(pk=user_id)
    else:
        user = None

    user_mailer.send_object(
        as_attachment=as_attachment, body=body,
        content_function_dotted_path=content_function_dotted_path,
        mime_type_function_dotted_path=mime_type_function_dotted_path,
        obj=obj, object_name=object_name,
        organization_installation_url=organization_installation_url,
        subject=subject, to=recipient, _user=user
    )
