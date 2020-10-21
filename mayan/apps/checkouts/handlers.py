from django.apps import apps

from .exceptions import DocumentNotCheckedOut, NewDocumentFileNotAllowed


def handler_check_new_file_creation(sender, instance, **kwargs):
    """
    Make sure that new file creation is allowed for this document
    """
    DocumentCheckout = apps.get_model(
        app_label='checkouts', model_name='DocumentCheckout'
    )

    try:
        checkout_information = DocumentCheckout.objects.get_check_out_info(
            document=instance.document
        )
    except DocumentNotCheckedOut:
        """No nothing"""
    else:
        if checkout_information.block_new_file:
            raise NewDocumentFileNotAllowed
