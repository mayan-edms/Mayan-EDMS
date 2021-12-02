from django_celery_beat.models import PeriodicTask

from mayan.apps.documents.tests.base import GenericDocumentTestCase

from .mixins.base_mixins import PeriodicSourceBackendTestMixin


class PeriodicSourceBackendTestCase(
    PeriodicSourceBackendTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    def test_periodic_source_delete(self):
        periodic_task_count = PeriodicTask.objects.count()

        self.test_source.delete()

        self.assertEqual(PeriodicTask.objects.count(), periodic_task_count - 1)

    def test_periodic_source_save(self):
        periodic_task_count = PeriodicTask.objects.count()

        self.test_source.save()

        self.assertEqual(PeriodicTask.objects.count(), periodic_task_count)
