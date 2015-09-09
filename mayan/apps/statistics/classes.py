from __future__ import unicode_literals

import json

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

    def __init__(self, slug, label, func, renderer):
        self.slug = slug
        self.label = label
        self.func = func
        self.renderer = renderer
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
        except StatisticResult.DoesNotExist:
            return {'series': {}}

    def get_chart_data(self):
        return self.renderer(data=self.get_results()).get_chart_data()


class ChartRenderer(object):
    def __init__(self, data):
        self.data = data

    def get_chart_data(self):
        raise NotImplementedError


class CharJSLine(ChartRenderer):
    template_name = 'statistics/backends/chartjs/line.html'

    dataset_palette = (
        {
            'fillColor': "rgba(220,220,220,0.2)",
            'strokeColor': "rgba(220,220,220,1)",
            'pointColor': "rgba(220,220,220,1)",
            'pointStrokeColor': "#fff",
            'pointHighlightFill': "#fff",
            'pointHighlightStroke': "rgba(220,220,220,1)",
        },
        {
            'fillColor': "rgba(151,187,205,0.2)",
            'strokeColor': "rgba(151,187,205,1)",
            'pointColor': "rgba(151,187,205,1)",
            'pointStrokeColor': "#fff",
            'pointHighlightFill': "#fff",
            'pointHighlightStroke': "rgba(151,187,205,1)",
        }
    )

    def get_chart_data(self):
        labels = []
        datasets = []

        for count, serie in enumerate(self.data['series'].items()):
            series_name, series_data = serie
            dataset_labels = []
            dataset_values = []

            for data_point in series_data:
                dataset_labels.extend(data_point.keys())
                dataset_values.extend(data_point.values())

            labels = dataset_labels
            dataset = {
                'label': series_name,
                'data': dataset_values,
            }
            dataset.update(
                CharJSLine.dataset_palette[
                    count % len(CharJSLine.dataset_palette)
                ]
            )

            datasets.append(dataset)

        data = {
            'labels': labels,
            'datasets': datasets,

        }

        return json.dumps(data)
