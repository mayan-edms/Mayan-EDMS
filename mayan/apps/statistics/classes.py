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

    def add_statistic(self, statistic):
        self._statistics.append(statistic)
        statistic.namespace = self

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
    def get(cls, name):
        return cls._registry[name]

    def __init__(self, name, label):
        self.name = name
        self.label = label
        self.__class__._registry[name] = self

    def __unicode__(self):
        return unicode(self.label)

    def get_results(self, *args, **kwargs):
        return NotImplementedError

    @property
    def id(self):
        return self.name
