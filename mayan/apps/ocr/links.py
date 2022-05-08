from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_document_type_ocr_settings, icon_document_type_ocr_submit,
    icon_document_version_ocr_content_multiple_delete,
    icon_document_version_ocr_content_single_delete,
    icon_document_version_ocr_content_detail,
    icon_document_version_ocr_content_download,
    icon_document_version_ocr_multiple_submit,
    icon_document_version_ocr_single_submit,
    icon_document_version_page_ocr_content_detail,
    icon_document_version_page_ocr_content_edit
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
    icon=icon_document_type_ocr_submit,
    permissions=(permission_document_version_ocr,),
    text=_('OCR documents per type'), view='ocr:document_type_submit'
)

# Document version

link_document_version_ocr_content_multiple_delete = Link(
    icon=icon_document_version_ocr_content_multiple_delete,
    text=_('Delete OCR content'),
    view='ocr:document_version_ocr_content_multiple_delete'
)
link_document_version_ocr_content_single_delete = Link(
    args='resolved_object.id',
    icon=icon_document_version_ocr_content_single_delete,
    permissions=(permission_document_version_ocr,),
    text=_('Delete OCR content'),
    view='ocr:document_version_ocr_content_single_delete'
)
link_document_version_ocr_content_detail = Link(
    args='resolved_object.id',
    icon=icon_document_version_ocr_content_detail,
    permissions=(permission_document_version_ocr_content_view,),
    text=_('OCR'), view='ocr:document_version_ocr_content_view'
)
link_document_version_ocr_content_download = Link(
    args='resolved_object.id',
    icon=icon_document_version_ocr_content_download,
    permissions=(permission_document_version_ocr_content_view,),
    text=_('Download OCR text'),
    view='ocr:document_version_ocr_content_download'
)
link_document_version_ocr_multiple_submit = Link(
    icon=icon_document_version_ocr_multiple_submit,
    text=_('Submit for OCR'), view='ocr:document_version_ocr_multiple_submit'
)
link_document_version_ocr_single_submit = Link(
    args='resolved_object.id',
    icon=icon_document_version_ocr_single_submit,
    permissions=(permission_document_version_ocr,), text=_('Submit for OCR'),
    view='ocr:document_version_ocr_single_submit'
)

# Document version page

link_document_version_page_ocr_content_detail_view = Link(
    args='resolved_object.id',
    icon=icon_document_version_page_ocr_content_detail,
    permissions=(permission_document_version_ocr_content_view,),
    text=_('OCR'), view='ocr:document_version_page_ocr_content_detail_view'
)
link_document_version_page_ocr_content_edit_view = Link(
    args='resolved_object.id',
    icon=icon_document_version_page_ocr_content_edit,
    permissions=(permission_document_version_ocr_content_edit,),
    text=_('Edit OCR'),
    view='ocr:document_version_page_ocr_content_edit_view'
)
