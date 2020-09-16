from django.apps import apps


def hook_is_new_file_allowed(document_file):
    NewVersionBlock = apps.get_model(
        app_label='checkouts', model_name='NewVersionBlock'
    )

    NewVersionBlock.objects.new_files_allowed(
        document=document_file.document
    )
