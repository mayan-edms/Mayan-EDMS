from django.contrib.humanize.templatetags.humanize import intcomma
from django.template import loader

from .icons import icon_dashboard_link_icon


class Dashboard:
    _registry = {}

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    def __init__(self, name, label):
        self.name = name
        self.label = label
        self.widgets = {}
        self.removed_widgets = []
        self.__class__._registry[name] = self

    def add_widget(self, widget, order=0):
        self.widgets[widget] = {'widget': widget, 'order': order}

    def get_widgets(self):
        """
        Returns a list of widgets sorted by their 'order'.
        If two or more widgets have the same 'order', sort by label.
        """
        return map(
            lambda x: x['widget'],
            filter(
                lambda x: x['widget'] not in self.removed_widgets,
                sorted(
                    self.widgets.values(),
                    key=lambda x: (x['order'], x['widget'].label)
                )
            )
        )

    def remove_widget(self, widget):
        self.removed_widgets.append(widget)

    def render(self, request):
        rendered_widgets = [
            widget().render(request=request) for widget in self.get_widgets()
        ]

        return loader.render_to_string(
            template_name='dashboards/dashboard.html', context={
                'widgets': rendered_widgets
            }
        )


class BaseDashboardWidget:
    _registry = {}
    context = {}
    template_name = None

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_all(cls):
        return cls._registry.items()

    @classmethod
    def register(cls, klass):
        cls._registry[klass.name] = klass

    def get_context(self):
        return self.context

    def render(self, request):
        if self.template_name:
            return loader.render_to_string(
                template_name=self.template_name, context=self.get_context(),
            )


class DashboardWidgetNumeric(BaseDashboardWidget):
    count = 0
    icon = None
    label = None
    link = None
    link_icon = icon_dashboard_link_icon
    template_name = 'dashboards/numeric_widget.html'

    def get_context(self):
        return {
            'count': intcomma(value=self.count),
            'count_raw': self.count,
            'icon': self.icon,
            'label': self.label,
            'link': self.link,
            'link_icon': self.link_icon
        }
