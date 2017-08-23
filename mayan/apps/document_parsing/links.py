from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import permission_content_view

link_document_content = Link(
    args='resolved_object.id', icon='fa fa-font',
    permissions=(permission_content_view,), text=_('Content'),
    view='document_parsing:document_content',
)
link_entry_list = Link(
    icon='fa fa-file-text-o', permissions=(permission_ocr_document,),
    text=_('Parsing errors'), view='document_parsing:entry_list'
)
link_document_content_errors_list = Link(
    args='resolved_object.id', icon='fa fa-file-text-o',
    permissions=(permission_ocr_content_view,), text=_('Parsing errors'),
    view='document_parsing:document_page_parsing_error_list'
)
link_document_content_download = Link(
    args='resolved_object.id', icon='fa fa-file-text-o',
    permissions=(permission_ocr_content_view,), text=_('Download content'),
    view='document_parsing:document_content_download'
)
