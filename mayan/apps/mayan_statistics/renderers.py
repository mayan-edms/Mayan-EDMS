from __future__ import unicode_literals

import json


class ChartRenderer(object):
    def __init__(self, data):
        self.data = data

    def get_chart_data(self):
        raise NotImplementedError


class ChartJSLine(ChartRenderer):
    template_name = 'statistics/renderers/chartjs/line.html'

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
        },
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
                ChartJSLine.dataset_palette[
                    count % len(ChartJSLine.dataset_palette)
                ]
            )

            datasets.append(dataset)

        data = {
            'labels': labels,
            'datasets': datasets,

        }

        return json.dumps(data)
