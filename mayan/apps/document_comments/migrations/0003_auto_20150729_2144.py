from django.db import migrations
from django.conf import settings


def operation_migrate_old_comments(apps, schema_editor):
    # https://code.djangoproject.com/ticket/24282
    # If someone has a better solution until Django 1.8, would appreciate
    # a pull-request :)

    try:
        from django.contrib.comments.models import Comment as OldComment
    except ImportError:
        # Django > 1.7
        pass
    else:

        Comment = apps.get_model(
            app_label='document_comments', model_name='Comment'
        )
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))

        for old_comment in OldComment.objects.using(schema_editor.connection.alias).all():
            comment = Comment(
                document=Document.objects.using(
                    schema_editor.connection.alias
                ).get(pk=old_comment.object_pk),
                user=User(old_comment.user.pk),
                comment=old_comment.comment,
                submit_date=old_comment.submit_date,
            )
            comment.save()


class Migration(migrations.Migration):
    dependencies = [
        ('document_comments', '0002_auto_20150729_2144'),
        ('documents', '0001_initial'),
        ('sites', '0001_initial'),
        ('contenttypes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL)
    ]

    operations = [
        migrations.RunPython(code=operation_migrate_old_comments),
    ]
