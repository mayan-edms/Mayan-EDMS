from ..classes import SourceBackend
from ..source_backends.mixins import (
    SourceBaseMixin, SourceBackendEmailMixin, SourceBackendPeriodicMixin
)


class SourceBackendSimple(SourceBaseMixin, SourceBackend):
    label = 'Test source backend'


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
        return self.process_message(message=self.content)
