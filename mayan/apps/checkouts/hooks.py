from django.apps import apps


def hook_is_new_file_allowed(document_file, document=None):
    NewFileBlock = apps.get_model(
        app_label='checkouts', model_name='NewFileBlock'
    )

    document = document or document_file.document

    NewFileBlock.objects.new_files_allowed(document=document)
