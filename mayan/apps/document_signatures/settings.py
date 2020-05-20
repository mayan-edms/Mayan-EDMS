import os

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import Namespace

from .setting_migrations import DocumentSignaturesSettingMigration

namespace = Namespace(
    label=_('Document signatures'),
    migration_class=DocumentSignaturesSettingMigration, name='signatures',
    version='0002'
)

setting_storage_backend = namespace.add_setting(
    default='django.core.files.storage.FileSystemStorage',
    global_name='SIGNATURES_STORAGE_BACKEND', help_text=_(
        'Path to the Storage subclass to use when storing detached '
        'signatures.'
    )
)
setting_storage_backend_arguments = namespace.add_setting(
    global_name='SIGNATURES_STORAGE_BACKEND_ARGUMENTS',
    default={
        'location': os.path.join(settings.MEDIA_ROOT, 'document_signatures')
    }, help_text=_(
        'Arguments to pass to the SIGNATURE_STORAGE_BACKEND. '
    )
)
