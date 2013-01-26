from django.utils.simplejson import dumps


class PropertyNamespace(object):
    _registry = {}

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_all(cls):
        return cls._registry.values()

    def __init__(self, name, label):
        self.name = name
        self.label = label
        self.properties = {}
        self.__class__._registry[name] = self

    def __unicode__(self):
        return unicode(self.label)

    def __str__(self):
        return str(self.label)

    def add_property(self, *args, **kwargs):
        prop = Property(*args, **kwargs)
        self.properties[prop.name] = prop

    def get_properties(self):
        return self.properties.values()

    @property
    def id(self):
        return self.name


class Property(object):
    _registry = {}

    @classmethod
    def get_all(cls):
        return cls._registry.values()

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_reportable(cls, as_dict=False, as_json=False):
        if as_json:
            return dumps(cls.get_reportable(as_dict=True))

        if not as_dict:
            return [prop for prop in cls.get_all() if prop.report]
        else:
            result = {}
            for prop in cls.get_all():
                if prop.report:
                    result[prop.name] = unicode(prop.value)
            return result

    def __init__(self, name, label, value, report=False):
        self.name = name
        self.label = label
        self.value = value
        self.report = report
        self.__class__._registry[name] = self

    def __unicode__(self):
        return unicode(self.value)

    def __str__(self):
        return str(self.value)
