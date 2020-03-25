from django.apps import apps


def hook_create_embedded_signature(document_version):
    EmbeddedSignature = apps.get_model(
        app_label='document_signatures', model_name='EmbeddedSignature'
    )

    EmbeddedSignature.objects.create(document_version=document_version)


def hook_decrypt_document_version(document_version, file_object):
    EmbeddedSignature = apps.get_model(
        app_label='document_signatures', model_name='EmbeddedSignature'
    )

    return {
        'file_object': EmbeddedSignature.objects.open_signed(
            document_version=document_version, file_object=file_object
        )
    }
