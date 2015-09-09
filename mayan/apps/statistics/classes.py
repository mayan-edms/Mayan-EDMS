from __future__ import unicode_literals

from .models import StatisticResult


class StatisticNamespace(object):
    _registry = {}

    @classmethod
    def get_all(cls):
        return cls._registry.values()

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    def __init__(self, name, label):
        self.name = name
        self.label = label
        self._statistics = []
        self.__class__._registry[name] = self

    def __unicode__(self):
        return unicode(self.label)

    def add_statistic(self, *args, **kwargs):
        statistic = Statistic(*args, **kwargs)
        statistic.namespace = self
        self._statistics.append(statistic)

    @property
    def id(self):
        return self.name

    @property
    def statistics(self):
        return self._statistics


class Statistic(object):
    _registry = {}

    @classmethod
    def get_all(cls):
        return cls._registry.values()

    @classmethod
    def get(cls, slug):
        return cls._registry[slug]

    def __init__(self, slug, label, func):
        self.slug = slug
        self.label = label
        self.func = func
        self.__class__._registry[slug] = self

    def __unicode__(self):
        return unicode(self.label)

    def execute(self):
        self.store_results(results=self.func())

    @property
    def id(self):
        return self.slug

    def store_results(self, results):
        StatisticResult.objects.filter(slug=self.slug).delete()

        statistic_result = StatisticResult.objects.create(slug=self.slug)
        statistic_result.store_data(data=results)

    def get_results(self):
        try:
            return StatisticResult.objects.get(slug=self.slug).get_data()
        except StatisticResultDoesNotExist:
            return ((),)
