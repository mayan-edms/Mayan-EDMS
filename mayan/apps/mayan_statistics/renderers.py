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
            'backgroundColor': 'rgba(24, 188, 156, 0.1)',
            'borderColor': '#18bc9c',
            'pointBorderWidth': 3,
            'pointHitRadius': 6,
            'pointHoverRadius': 7,
            'pointRadius': 6,

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
