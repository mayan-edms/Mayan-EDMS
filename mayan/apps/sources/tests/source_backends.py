from ..classes import SourceBackend
from ..source_backends.email_backends import SourceBackendEmailMixin
from ..source_backends.mixins import (
    SourceBaseMixin, SourceBackendPeriodicMixin
)

__all__ = (
    'SourceBackendSimple', 'SourceBackendTestPeriodic',
    'SourceBackendTestEmail'
)


class SourceBackendSimple(SourceBaseMixin, SourceBackend):
    label = 'Test source backend'

    def process_documents(self, dry_run=False):
        """Do nothing. This method is added to allow view testing."""


class SourceBackendTestPeriodic(
    SourceBackendPeriodicMixin, SourceBaseMixin, SourceBackend
):
    label = 'Test periodic source backend'


class SourceBackendTestEmail(
    SourceBackendEmailMixin, SourceBackendPeriodicMixin, SourceBaseMixin,
    SourceBackend
):
    label = 'Test email source backend'

    def get_shared_uploaded_files(self):
        data = self.get_model_instance().get_backend_data()

        message = getattr(self, 'content', data.get('_test_content'))

        return self.process_message(message=message)
