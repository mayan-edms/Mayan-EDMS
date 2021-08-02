from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_entry_list, icon_document_type_ocr_settings,
    icon_document_type_submit, icon_document_version_multiple_ocr_submit,
    icon_document_version_page_ocr_content_detail_view,
    icon_document_version_ocr_content_delete,
    icon_document_version_ocr_content_view,
    icon_document_version_ocr_download,
    icon_document_version_ocr_errors_list, icon_document_version_ocr_submit
)
from .permissions import (
    permission_document_version_ocr_content_view, permission_document_version_ocr,
    permission_document_type_ocr_setup
)

# Document type

link_document_type_ocr_settings = Link(
    args='resolved_object.id',
    icon=icon_document_type_ocr_settings,
    permissions=(permission_document_type_ocr_setup,), text=_('Setup OCR'),
    view='ocr:document_type_ocr_settings'
)
link_document_type_submit = Link(
    icon=icon_document_type_submit,
    permissions=(permission_document_version_ocr,),
    text=_('OCR documents per type'), view='ocr:document_type_submit'
)

# Document version page

link_document_version_ocr_content_view = Link(
    args='resolved_object.id',
    icon=icon_document_version_ocr_content_view,
    permissions=(permission_document_version_ocr_content_view,),
    text=_('OCR'), view='ocr:document_version_ocr_content_view'
)
link_document_version_ocr_content_delete = Link(
    args='resolved_object.id',
    icon=icon_document_version_ocr_content_delete,
    permissions=(permission_document_version_ocr,),
    text=_('Delete OCR content'),
    view='ocr:document_version_ocr_content_delete'
)
link_document_version_multiple_ocr_content_delete = Link(
    icon=icon_document_version_ocr_content_delete,
    text=_('Delete OCR content'),
    view='ocr:document_version_multiple_ocr_content_delete'
)
link_document_version_ocr_submit = Link(
    args='resolved_object.id',
    icon=icon_document_version_ocr_submit,
    permissions=(permission_document_version_ocr,), text=_('Submit for OCR'),
    view='ocr:document_version_ocr_submit'
)
link_document_version_multiple_ocr_submit = Link(
    icon=icon_document_version_multiple_ocr_submit,
    text=_('Submit for OCR'), view='ocr:document_version_multiple_ocr_submit'
)
link_document_version_ocr_errors_list = Link(
    args='resolved_object.id',
    icon=icon_document_version_ocr_errors_list,
    permissions=(permission_document_version_ocr_content_view,),
    text=_('OCR errors'), view='ocr:document_version_ocr_error_list'
)
link_document_version_ocr_download = Link(
    args='resolved_object.id', icon=icon_document_version_ocr_download,
    permissions=(permission_document_version_ocr_content_view,),
    text=_('Download OCR text'), view='ocr:document_version_ocr_download'
)

# Document version page

link_document_version_page_ocr_content_detail_view = Link(
    args='resolved_object.id',
    icon=icon_document_version_page_ocr_content_detail_view,
    permissions=(permission_document_version_ocr_content_view,),
    text=_('OCR'), view='ocr:document_version_page_ocr_content_detail_view'
)

# Other

link_entry_list = Link(
    icon=icon_entry_list,
    permissions=(permission_document_version_ocr,), text=_('OCR errors'),
    view='ocr:entry_list'
)
