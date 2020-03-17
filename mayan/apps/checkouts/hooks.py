from __future__ import unicode_literals

from django.apps import apps


def hook_is_new_version_allowed(document_version):
    NewVersionBlock = apps.get_model(
        app_label='checkouts', model_name='NewVersionBlock'
    )

    NewVersionBlock.objects.new_versions_allowed(
        document=document_version.document
    )
