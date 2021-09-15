from mayan.apps.documents.literals import DOCUMENT_VERSION_EXPORT_MIMETYPE
from mayan.apps.storage.utils import NamedTemporaryFile

from .literals import EMAIL_SEPARATORS


def split_recipient_list(recipients, separator_list=None, separator_index=0):
    separator_list = separator_list or EMAIL_SEPARATORS

    try:
        separator = separator_list[separator_index]
    except IndexError:
        return recipients
    else:
        result = []
        for recipient in recipients:
            result.extend(recipient.split(separator))

        return split_recipient_list(
            recipients=result, separator_list=separator_list,
            separator_index=separator_index + 1
        )


def get_document_file_content(obj):
    return obj.open()


def get_document_file_mime_type(obj):
    return obj.mimetype


def get_document_version_content(obj):
    class TemporaryExportedDocumentVersion:
        def __init__(self, obj):
            self.obj = obj

        def __enter__(self):
            self.file_object = NamedTemporaryFile(delete=False)
            obj.export(file_object=self.file_object)
            self.file_object.seek(0)
            return self.file_object

        def __exit__(self, *exc):
            self.file_object.close()

    return TemporaryExportedDocumentVersion(obj=obj)


def get_document_version_mime_type(obj):
    return DOCUMENT_VERSION_EXPORT_MIMETYPE
