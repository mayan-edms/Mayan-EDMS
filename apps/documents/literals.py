from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission


PICTURE_ERROR_SMALL = u'picture_error.png'
PICTURE_ERROR_MEDIUM = u'1297211435_error.png'
PICTURE_UNKNOWN_SMALL = u'1299549572_unknown2.png'
PICTURE_UNKNOWN_MEDIUM = u'1299549805_unknown.png'

document_namespace = PermissionNamespace('documents', _(u'Documents'))

PERMISSION_DOCUMENT_CREATE = Permission.objects.register(document_namespace, 'document_create', _(u'Create documents'))
PERMISSION_DOCUMENT_PROPERTIES_EDIT = Permission.objects.register(document_namespace, 'document_properties_edit', _(u'Edit document properties'))
PERMISSION_DOCUMENT_EDIT = Permission.objects.register(document_namespace, 'document_edit', _(u'Edit documents'))
PERMISSION_DOCUMENT_VIEW = Permission.objects.register(document_namespace, 'document_view', _(u'View documents'))
PERMISSION_DOCUMENT_DELETE = Permission.objects.register(document_namespace, 'document_delete', _(u'Delete documents'))
PERMISSION_DOCUMENT_DOWNLOAD = Permission.objects.register(document_namespace, 'document_download', _(u'Download documents'))
PERMISSION_DOCUMENT_TRANSFORM = Permission.objects.register(document_namespace, 'document_transform', _(u'Transform documents'))
PERMISSION_DOCUMENT_TOOLS = Permission.objects.register(document_namespace, 'document_tools', _(u'Execute document modifying tools'))
PERMISSION_DOCUMENT_VERSION_REVERT = Permission.objects.register(document_namespace, 'document_version_revert', _(u'Revert documents to a previous version'))

documents_setup_namespace = PermissionNamespace('documents_setup', _(u'Documents setup'))

PERMISSION_DOCUMENT_TYPE_VIEW = Permission.objects.register(documents_setup_namespace, 'document_type_view', _(u'View document types'))
PERMISSION_DOCUMENT_TYPE_EDIT = Permission.objects.register(documents_setup_namespace, 'document_type_edit', _(u'Edit document types'))
PERMISSION_DOCUMENT_TYPE_DELETE = Permission.objects.register(documents_setup_namespace, 'document_type_delete', _(u'Delete document types'))
PERMISSION_DOCUMENT_TYPE_CREATE = Permission.objects.register(documents_setup_namespace, 'document_type_create', _(u'Create document types'))


HISTORY_DOCUMENT_CREATED = {
    'namespace': 'documents', 'name': 'document_created',
    'label': _(u'Document creation'),
    'summary': _(u'Document "%(content_object)s" created by %(fullname)s.'),
    'details': _(u'Document "%(content_object)s" created on %(datetime)s by %(fullname)s.'),
    'expressions': {'fullname': 'user.get_full_name() if user.get_full_name() else user.username'}
}

HISTORY_DOCUMENT_EDITED = {
    'namespace': 'documents', 'name': 'document_edited',
    'label': _(u'Document edited'),
    'summary': _(u'Document "%(content_object)s" edited by %(fullname)s.'),
    'details': _(u'Document "%(content_object)s" was edited on %(datetime)s by %(fullname)s.  The following changes took place: %(changes)s.'),
    'expressions': {
        'fullname': 'user.get_full_name() if user.get_full_name() else user.username',
        'changes': 'u\', \'.join([\'"%s": "%s" -> "%s"\' % (key, value[\'old_value\'], value[\'new_value\']) for key, value in diff.items()])'
    }
}

HISTORY_DOCUMENT_DELETED = {
    'namespace': 'documents', 'name': 'document_deleted',
    'label': _(u'Document deleted'),
    'summary': _(u'Document "%(document)s" deleted by %(fullname)s.'),
    'details': _(u'Document "%(document)s" deleted on %(datetime)s by %(fullname)s.'),
    'expressions': {'fullname': 'user.get_full_name() if user.get_full_name() else user.username'}
}

RELEASE_LEVEL_FINAL = 1
RELEASE_LEVEL_ALPHA = 2
RELEASE_LEVEL_BETA = 3
RELEASE_LEVEL_RC = 4
RELEASE_LEVEL_HF = 5

RELEASE_LEVEL_CHOICES = (
    (RELEASE_LEVEL_FINAL, _(u'final')),
    (RELEASE_LEVEL_ALPHA, _(u'alpha')),
    (RELEASE_LEVEL_BETA, _(u'beta')),
    (RELEASE_LEVEL_RC, _(u'release candidate')),
    (RELEASE_LEVEL_HF, _(u'hotfix')),
)

VERSION_UPDATE_MAJOR = u'major'
VERSION_UPDATE_MINOR = u'minor'
VERSION_UPDATE_MICRO = u'micro'
