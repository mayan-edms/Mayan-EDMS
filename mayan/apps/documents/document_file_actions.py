from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from .classes import DocumentFileAction


class DocumentFileActionAppendNewPages(DocumentFileAction):
    action_id = 2
    label = _('Append. Create a new version and append the new file pages.')

    @staticmethod
    def execute(document, document_file, comment, _user):
        DocumentVersion = apps.get_model(
            app_label='documents', model_name='DocumentVersion'
        )

        annotated_content_object_list = []
        annotated_content_object_list.extend(
            DocumentVersion.annotate_content_object_list(
                content_object_list=document.version_active.page_content_objects
            )
        )

        annotated_content_object_list.extend(
            DocumentVersion.annotate_content_object_list(
                content_object_list=document_file.pages.all(),
                start_page_number=document.version_active.pages.count() + 1
            )
        )

        document_version = DocumentVersion(
            document=document, comment=comment
        )
        document_version._event_actor = _user
        document_version.save()

        document_version.pages_remap(
            annotated_content_object_list=annotated_content_object_list,
            _user=_user
        )


class DocumentFileActionNothing(DocumentFileAction):
    action_id = 3
    label = _(
        'Keep. Do not create a new version and keep the current '
        'version pages.'
    )

    @staticmethod
    def execute(document, document_file, comment, _user):
        return


class DocumentFileActionUseNewPages(DocumentFileAction):
    action_id = 1
    label = _('Replace. Create a new version and use the new file pages.')

    @staticmethod
    def execute(document, document_file, comment, _user):
        DocumentVersion = apps.get_model(
            app_label='documents', model_name='DocumentVersion'
        )

        document_version = DocumentVersion(
            document=document, comment=comment
        )
        document_version._event_actor = _user
        document_version.save()

        annotated_content_object_list = DocumentVersion.annotate_content_object_list(
            content_object_list=document_file.pages.all()
        )

        document_version.pages_remap(
            annotated_content_object_list=annotated_content_object_list,
            _user=_user
        )
