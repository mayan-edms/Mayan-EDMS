from __future__ import unicode_literals

from django.template.loader import get_template


class IconDriver(object):
    _registry = {}

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def register(cls, driver_class):
        cls._registry[driver_class.name] = driver_class


class FontAwesomeDriver(IconDriver):
    name = 'fontawesome'
    template_name = 'appearance/icons/font_awesome_symbol.html'

    def __init__(self, symbol):
        self.symbol = symbol

    def render(self):
        return get_template(self.template_name).render(
            context={'symbol': self.symbol}
        )


class FontAwesomeCSSDriver(IconDriver):
    name = 'fontawesomecss'
    template_name = 'appearance/icons/font_awesome_css.html'

    def __init__(self, css_classes):
        self.css_classes = css_classes

    def render(self):
        return get_template(self.template_name).render(
            context={'css_classes': self.css_classes}
        )


class Icon(object):
    def __init__(self, driver_name, **kwargs):
        self.driver = IconDriver.get(name=driver_name)(**kwargs)

    def render(self, **kwargs):
        return self.driver.render(**kwargs)


IconDriver.register(driver_class=FontAwesomeDriver)
IconDriver.register(driver_class=FontAwesomeCSSDriver)
