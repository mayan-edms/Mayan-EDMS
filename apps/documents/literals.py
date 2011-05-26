from django.utils.translation import ugettext_lazy as _

PICTURE_ERROR_SMALL = u'picture_error.png'
PICTURE_ERROR_MEDIUM = u'1297211435_error.png'
PICTURE_UNKNOWN_SMALL = u'1299549572_unknown2.png'
PICTURE_UNKNOWN_MEDIUM = u'1299549805_unknown.png'

PERMISSION_DOCUMENT_CREATE = {'namespace': 'documents', 'name': 'document_create', 'label': _(u'Create document')}
PERMISSION_DOCUMENT_PROPERTIES_EDIT = {'namespace': 'documents', 'name': 'document_properties_edit', 'label': _(u'Edit document properties')}
PERMISSION_DOCUMENT_EDIT = {'namespace': 'documents', 'name': 'document_edit', 'label': _(u'Edit document')}
PERMISSION_DOCUMENT_VIEW = {'namespace': 'documents', 'name': 'document_view', 'label': _(u'View document')}
PERMISSION_DOCUMENT_DELETE = {'namespace': 'documents', 'name': 'document_delete', 'label': _(u'Delete document')}
PERMISSION_DOCUMENT_DOWNLOAD = {'namespace': 'documents', 'name': 'document_download', 'label': _(u'Download document')}
PERMISSION_DOCUMENT_TRANSFORM = {'namespace': 'documents', 'name': 'document_transform', 'label': _(u'Transform document')}
PERMISSION_DOCUMENT_TOOLS = {'namespace': 'documents', 'name': 'document_tools', 'label': _(u'Execute document modifying tools')}

UPLOAD_SOURCE_LOCAL = u'local'
UPLOAD_SOURCE_STAGING = u'staging'
UPLOAD_SOURCE_USER_STAGING = u'user_staging'

HISTORY_DOCUMENT_CREATED = {
    'namespace': 'documents', 'name': 'document_created',
    'label': _(u'Document creation'),
    'summary': _(u'Document: %(content_object)s created by %(fullname)s.'),
    'details': _(u'Document: %(content_object)s created on %(datetime)s by %(fullname)s.'),
    'expressions': [{'fullname': 'user.get_full_name() if user.get_full_name() else user.username'}]
}

HISTORY_DOCUMENT_EDITED = {
    'namespace': 'documents', 'name': 'document_edited',
    'label': _(u'Document edited'),
    'summary': _(u'Document: %(content_object)s edited by %(fullname)s.'),
    'details': _(u'Document: %(content_object)s edited on %(datetime)s by %(fullname)s.'),
    'expressions': [{'fullname': 'user.get_full_name() if user.get_full_name() else user.username'}]
}
