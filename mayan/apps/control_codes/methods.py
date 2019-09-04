from __future__ import unicode_literals

from .tasks import task_process_document_version


def method_document_submit(self):
    latest_version = self.latest_version
    # Don't error out if document has no version
    if latest_version:
        latest_version.submit_for_control_codes_processing()


def method_document_version_submit(self):
    task_process_document_version.apply_async(
        kwargs={
            'document_version_id': self.pk,
        }
    )
