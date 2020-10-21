from django.apps import apps

from .exceptions import DocumentNotCheckedOut, NewDocumentFileNotAllowed


def hook_is_new_file_allowed(document_file, document=None):
    DocumentCheckout = apps.get_model(
        app_label='checkouts', model_name='DocumentCheckout'
    )

    document = document or document_file.document

    try:
        checkout_information = DocumentCheckout.objects.get_check_out_info(
            document=document
        )
    except DocumentNotCheckedOut:
        """No nothing"""
    else:
        if checkout_information.block_new_file:
            raise NewDocumentFileNotAllowed

