from __future__ import unicode_literals

from django.core import management

from django_celery_beat.models import IntervalSchedule, PeriodicTask


class Command(management.BaseCommand):
    help = 'Removes all periodic tasks.'

    def handle(self, *args, **options):
        PeriodicTask.objects.all().delete()
        IntervalSchedule.objects.all().delete()
