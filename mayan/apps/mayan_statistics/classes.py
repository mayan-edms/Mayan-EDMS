from django.apps import apps
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from celery.schedules import crontab

from mayan.celery import app

from .renderers import ChartJSLine


class StatisticNamespace:
    _registry = {}

    @classmethod
    def get_all(cls):
        return list(cls._registry.values())

    @classmethod
    def get(cls, slug):
        return cls._registry[slug]

    def __init__(self, slug, label):
        self.slug = slug
        self.label = label
        self._statistics = []
        self.__class__._registry[slug] = self

    def __str__(self):
        return force_text(self.label)

    def add_statistic(self, klass, *args, **kwargs):
        statistic = klass(*args, **kwargs)
        statistic.namespace = self
        self._statistics.append(statistic)

    @property
    def statistics(self):
        return self._statistics


class Statistic:
    _registry = {}
    renderer = None

    @staticmethod
    def evaluate(data):
        try:
            for key, value in data.items():
                return {key: Statistic.evaluate(data=value)}
        except AttributeError:
            if type(data) == map:
                data = list(data)

        return data

    @staticmethod
    def purge_schedules():
        PeriodicTask = apps.get_model(
            app_label='django_celery_beat', model_name='PeriodicTask'
        )
        StatisticResult = apps.get_model(
            app_label='mayan_statistics', model_name='StatisticResult'
        )

        queryset = PeriodicTask.objects.filter(
            name__startswith='mayan_statistics.'
        ).exclude(name__in=Statistic.get_task_names())

        for periodic_task in queryset:
            crontab_instance = periodic_task.crontab
            periodic_task.delete()

            if crontab_instance and not crontab_instance.periodictask_set.all():
                # Only delete the interval if nobody else is using it
                crontab_instance.delete()

        StatisticResult.objects.filter(
            slug__in=queryset.values_list('name', flat=True)
        ).delete()

    @classmethod
    def get(cls, slug):
        return cls._registry[slug]

    @classmethod
    def get_all(cls):
        return list(cls._registry.values())

    @classmethod
    def get_task_names(cls):
        return [task.get_task_name() for task in cls.get_all()]

    def __init__(self, slug, label, func, minute='*', hour='*', day_of_week='*', day_of_month='*', month_of_year='*'):
        from .queues import queue_statistics, task_execute_statistic

        self.slug = slug
        self.label = label
        self.func = func

        self.schedule = crontab(
            minute=minute, hour=hour, day_of_week=day_of_week,
            day_of_month=day_of_month, month_of_year=month_of_year,
        )

        app.conf.beat_schedule.update(
            {
                self.get_task_name(): {
                    'task': task_execute_statistic.dotted_path,
                    'schedule': self.schedule,
                    'args': (self.slug,)
                },
            }
        )

        app.conf.task_routes.update(
            {
                self.get_task_name(): {
                    'queue': queue_statistics.name
                },
            }
        )

        self.__class__._registry[slug] = self

    def __str__(self):
        return force_text(self.label)

    def execute(self):
        results = self.func()
        # Force evaluation of results to be able to store it serialized
        # Needed for Python 3
        # PY3
        results = Statistic.evaluate(data=results)
        self.store_results(results=results)

    def get_chart_data(self):
        return self.renderer(data=self.get_results_data()).get_chart_data()

    def get_last_update(self):
        results = self.get_results()

        if results:
            return results.datetime
        else:
            return _('Never')

    def get_results(self, only=None):
        StatisticResult = apps.get_model(
            app_label='mayan_statistics', model_name='StatisticResult'
        )

        try:
            return StatisticResult.objects.get(slug=self.slug)
        except StatisticResult.DoesNotExist:
            return StatisticResult.objects.none()
        except StatisticResult.MultipleObjectsReturned:
            # This should not happen. Self-heal by deleting the duplicate
            # results.
            StatisticResult.objects.filter(slug=self.slug).delete()
            return StatisticResult.objects.none()

    def get_results_data(self):
        results = self.get_results()

        if results:
            return results.get_data()
        else:
            return {'series': {}}

    def get_task_name(self):
        return 'mayan_statistics.task_execute_statistic_{}'.format(self.slug)

    def store_results(self, results):
        StatisticResult = apps.get_model(
            app_label='mayan_statistics', model_name='StatisticResult'
        )

        StatisticResult.objects.filter(slug=self.slug).delete()

        statistic_result, created = StatisticResult.objects.get_or_create(
            slug=self.slug
        )
        statistic_result.store_data(data=results)


class StatisticLineChart(Statistic):
    renderer = ChartJSLine
