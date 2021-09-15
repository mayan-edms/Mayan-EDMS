from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_entry_list, icon_document_type_ocr_settings,
    icon_document_type_submit,
    icon_document_version_ocr_content_delete_multiple,
    icon_document_version_ocr_content_delete_single,
    icon_document_version_ocr_content_view,
    icon_document_version_ocr_download,
    icon_document_version_ocr_errors_list,
    icon_document_version_ocr_submit_multiple,
    icon_document_version_ocr_submit_single,
    icon_document_version_page_ocr_content_detail_view,
    icon_document_version_page_ocr_content_edit_view
)
from .permissions import (
    permission_document_type_ocr_setup, permission_document_version_ocr,
    permission_document_version_ocr_content_edit,
    permission_document_version_ocr_content_view
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

# Document version

link_document_version_ocr_content_delete_multiple = Link(
    icon=icon_document_version_ocr_content_delete_multiple,
    text=_('Delete OCR content'),
    view='ocr:document_version_ocr_content_delete_multiple'
)
link_document_version_ocr_content_delete_single = Link(
    args='resolved_object.id',
    icon=icon_document_version_ocr_content_delete_single,
    permissions=(permission_document_version_ocr,),
    text=_('Delete OCR content'),
    view='ocr:document_version_ocr_content_delete_single'
)
link_document_version_ocr_content_view = Link(
    args='resolved_object.id',
    icon=icon_document_version_ocr_content_view,
    permissions=(permission_document_version_ocr_content_view,),
    text=_('OCR'), view='ocr:document_version_ocr_content_view'
)
link_document_version_ocr_download = Link(
    args='resolved_object.id', icon=icon_document_version_ocr_download,
    permissions=(permission_document_version_ocr_content_view,),
    text=_('Download OCR text'), view='ocr:document_version_ocr_download'
)
link_document_version_ocr_errors_list = Link(
    args='resolved_object.id',
    icon=icon_document_version_ocr_errors_list,
    permissions=(permission_document_version_ocr_content_view,),
    text=_('OCR errors'), view='ocr:document_version_ocr_error_list'
)
link_document_version_ocr_submit_multiple = Link(
    icon=icon_document_version_ocr_submit_multiple,
    text=_('Submit for OCR'), view='ocr:document_version_ocr_submit_multiple'
)
link_document_version_ocr_submit_single = Link(
    args='resolved_object.id',
    icon=icon_document_version_ocr_submit_single,
    permissions=(permission_document_version_ocr,), text=_('Submit for OCR'),
    view='ocr:document_version_ocr_submit_single'
)

# Document version page

link_document_version_page_ocr_content_detail_view = Link(
    args='resolved_object.id',
    icon=icon_document_version_page_ocr_content_detail_view,
    permissions=(permission_document_version_ocr_content_view,),
    text=_('OCR'), view='ocr:document_version_page_ocr_content_detail_view'
)
link_document_version_page_ocr_content_edit_view = Link(
    args='resolved_object.id',
    icon=icon_document_version_page_ocr_content_edit_view,
    permissions=(permission_document_version_ocr_content_edit,),
    text=_('Edit OCR'), view='ocr:document_version_page_ocr_content_edit_view'
)

# Other

link_entry_list = Link(
    icon=icon_entry_list,
    permissions=(permission_document_version_ocr,), text=_('OCR errors'),
    view='ocr:entry_list'
)
