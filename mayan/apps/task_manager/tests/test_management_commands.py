from django.core import management

from django_celery_beat.models import IntervalSchedule, PeriodicTask

from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import TaskManagerManagementCommandTestMixin


class TaskManagerManagementCommandTestCase(
    TaskManagerManagementCommandTestMixin, BaseTestCase
):
    def test_purge_periodic_tasks_management_command(self):
        self._test_interval_schedule_count = IntervalSchedule.objects.count()
        self._test_periodic_task_count = PeriodicTask.objects.count()

        self._clear_events()

        management.call_command(
            command_name='task_manager_purge_periodic_tasks'
        )

        self.assertEqual(
            IntervalSchedule.objects.count(),
            self._test_interval_schedule_count - 1
        )
        self.assertEqual(
            PeriodicTask.objects.count(),
            self._test_periodic_task_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
