from django.apps import apps


def hook_create_embedded_signature(document_file):
    EmbeddedSignature = apps.get_model(
        app_label='document_signatures', model_name='EmbeddedSignature'
    )

    EmbeddedSignature.objects.create(document_file=document_file)


def hook_decrypt_document_file(document_file, file_object):
    EmbeddedSignature = apps.get_model(
        app_label='document_signatures', model_name='EmbeddedSignature'
    )

    return {
        'file_object': EmbeddedSignature.objects.open_signed(
            document_file=document_file, file_object=file_object
        )
    }
