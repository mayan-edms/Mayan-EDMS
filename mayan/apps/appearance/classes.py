from __future__ import unicode_literals

from django.template import Context, Template


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
    template_text = '<i class="hidden-xs hidden-sm hidden-md fa fa-{{ symbol }}"></i>'

    def __init__(self, symbol):
        self.symbol = symbol

    def render(self):
        return Template(self.template_text).render(
            context=Context({'symbol': self.symbol})
        )


class Icon(object):
    def __init__(self, driver_name, **kwargs):
        self.driver = IconDriver.get(name=driver_name)(**kwargs)

    def render(self, **kwargs):
        return self.driver.render(**kwargs)


IconDriver.register(driver_class=FontAwesomeDriver)
