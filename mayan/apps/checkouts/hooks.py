from django.apps import apps


def hook_is_new_file_allowed(document_file):
    NewFileBlock = apps.get_model(
        app_label='checkouts', model_name='NewFileBlock'
    )

    NewFileBlock.objects.new_files_allowed(
        document=document_file.document
    )
