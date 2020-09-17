from django.apps import apps

from .exceptions import NewDocumentFileNotAllowed


def handler_check_new_file_creation(sender, instance, **kwargs):
    """
    Make sure that new file creation is allowed for this document
    """
    NewFileBlock = apps.get_model(
        app_label='checkouts', model_name='NewFileBlock'
    )
    if NewFileBlock.objects.is_blocked(document=instance.document) and not instance.pk:
        # Block only new files (no pk), not existing file being updated.
        raise NewDocumentFileNotAllowed
