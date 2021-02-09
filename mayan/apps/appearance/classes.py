from django.template.loader import get_template


class IconDriver:
    context = {}
    _registry = {}

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def register(cls, driver_class):
        cls._registry[driver_class.name] = driver_class

    def get_context(self):
        return self.context

    def render(self, extra_context=None):
        context = self.get_context()
        if extra_context:
            context.update(extra_context)
        return get_template(template_name=self.template_name).render(
            context=context
        )


class FontAwesomeDriver(IconDriver):
    name = 'fontawesome'
    template_name = 'appearance/icons/font_awesome_symbol.html'

    def __init__(self, symbol):
        self.symbol = symbol

    def get_context(self):
        return {'symbol': self.symbol}


class FontAwesomeDualClassesDriver(IconDriver):
    name = 'fontawesome-dual-classes'
    template_name = 'appearance/icons/font_awesome_layers.html'

    def __init__(self, primary_class, secondary_class):
        self.primary_class = primary_class
        self.secondary_class = secondary_class

    def get_context(self):
        return {
            'data': (
                {
                    'class': 'fas fa-circle',
                    'transform': 'down-3 right-10',
                    'mask': '{}'.format(self.primary_class)
                },
                {'class': 'far fa-circle', 'transform': 'down-3 right-10'},
                {
                    'class': '{}'.format(self.secondary_class),
                    'transform': 'shrink-4 down-3 right-10'
                },
            )
        }


class FontAwesomeDualDriver(IconDriver):
    name = 'fontawesome-dual'
    template_name = 'appearance/icons/font_awesome_layers.html'

    def __init__(self, primary_symbol, secondary_symbol):
        self.primary_symbol = primary_symbol
        self.secondary_symbol = secondary_symbol

    def get_context(self):
        return {
            'data': (
                {
                    'class': 'fas fa-circle',
                    'transform': 'down-3 right-10',
                    'mask': 'fas fa-{}'.format(self.primary_symbol)
                },
                {'class': 'far fa-circle', 'transform': 'down-3 right-10'},
                {
                    'class': 'fas fa-{}'.format(self.secondary_symbol),
                    'transform': 'shrink-4 down-3 right-10'
                },
            )
        }


class FontAwesomeCSSDriver(IconDriver):
    name = 'fontawesomecss'
    template_name = 'appearance/icons/font_awesome_css.html'

    def __init__(self, css_classes):
        self.css_classes = css_classes

    def get_context(self):
        return {'css_classes': self.css_classes}


class FontAwesomeMasksDriver(IconDriver):
    name = 'fontawesome-masks'
    template_name = 'appearance/icons/font_awesome_masks.html'

    def __init__(self, data):
        self.data = data

    def get_context(self):
        return {'data': self.data}


class FontAwesomeLayersDriver(IconDriver):
    name = 'fontawesome-layers'
    template_name = 'appearance/icons/font_awesome_layers.html'

    def __init__(self, data):
        self.data = data

    def get_context(self):
        return {
            'data': self.data,
        }


class Icon:
    def __init__(self, driver_name, **kwargs):
        self.kwargs = kwargs
        self.driver = IconDriver.get(name=driver_name)(**kwargs)

    def render(self, **kwargs):
        return self.driver.render(**kwargs)


IconDriver.register(driver_class=FontAwesomeCSSDriver)
IconDriver.register(driver_class=FontAwesomeDriver)
IconDriver.register(driver_class=FontAwesomeDualClassesDriver)
IconDriver.register(driver_class=FontAwesomeDualDriver)
IconDriver.register(driver_class=FontAwesomeLayersDriver)
IconDriver.register(driver_class=FontAwesomeMasksDriver)
