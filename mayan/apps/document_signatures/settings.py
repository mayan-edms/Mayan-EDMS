from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_SIGNATURES_STORAGE_BACKEND,
    DEFAULT_SIGNATURES_STORAGE_BACKEND_ARGUMENTS
)
from .setting_migrations import DocumentSignaturesSettingMigration

namespace = SettingNamespace(
    label=_('Document signatures'),
    migration_class=DocumentSignaturesSettingMigration, name='signatures',
    version='0002'
)

setting_storage_backend = namespace.add_setting(
    default=DEFAULT_SIGNATURES_STORAGE_BACKEND,
    global_name='SIGNATURES_STORAGE_BACKEND', help_text=_(
        'Path to the Storage subclass to use when storing detached '
        'signatures.'
    )
)
setting_storage_backend_arguments = namespace.add_setting(
    default=DEFAULT_SIGNATURES_STORAGE_BACKEND_ARGUMENTS,
    global_name='SIGNATURES_STORAGE_BACKEND_ARGUMENTS', help_text=_(
        'Arguments to pass to the SIGNATURE_STORAGE_BACKEND.'
    )
)
