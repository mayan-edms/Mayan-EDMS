from django.utils.translation import ugettext_lazy as _

from .events import event_file_metadata_document_version_submit
from .tasks import task_process_document_version


def method_document_submit(self):
    latest_version = self.latest_version
    # Don't error out if document has no version
    if latest_version:
        latest_version.submit_for_file_metadata_processing()


def method_document_version_submit(self):
    event_file_metadata_document_version_submit.commit(
        action_object=self.document, target=self
    )

    task_process_document_version.apply_async(
        kwargs={
            'document_version_id': self.pk,
        }
    )


def method_get_document_file_metadata(self, dotted_name):
    latest_version = self.latest_version
    # Don't error out if document has no version
    if latest_version:
        return latest_version.get_file_metadata(
            dotted_name=dotted_name
        )


method_get_document_file_metadata.short_description = _(
    'get_file_metadata(< file metadata dotted path >)'
)
method_get_document_file_metadata.help_text = _(
    'Return the specified document file metadata entry.'
)


def method_get_document_version_file_metadata(self, dotted_name):
    parts = dotted_name.split('.', 1)

    if len(parts) < 2:
        return

    driver_internal_name = parts[0]
    key = parts[1].replace('.', '_')

    try:
        document_driver = self.file_metadata_drivers.get(
            driver__internal_name=driver_internal_name
        )
    except self.file_metadata_drivers.model.DoesNotExist:
        return
    else:
        try:
            return document_driver.entries.get(key=key).value
        except document_driver.entries.model.DoesNotExist:
            return


method_get_document_version_file_metadata.help_text = _(
    'Return the specified document version file metadata entry.'
)
