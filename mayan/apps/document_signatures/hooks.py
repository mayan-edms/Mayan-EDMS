from django.apps import apps


def hook_create_embedded_signature(instance):
    EmbeddedSignature = apps.get_model(
        app_label='document_signatures', model_name='EmbeddedSignature'
    )

    EmbeddedSignature.objects.create(document_file=instance)


def hook_decrypt_document_file(instance, file_object):
    EmbeddedSignature = apps.get_model(
        app_label='document_signatures', model_name='EmbeddedSignature'
    )

    return {
        'file_object': EmbeddedSignature.objects.open_signed(
            document_file=instance, file_object=file_object
        )
    }
