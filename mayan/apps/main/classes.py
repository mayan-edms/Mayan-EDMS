class MissingItem(object):
    _registry = []

    @classmethod
    def get_all(cls):
        return cls._registry

    def __init__(self, label, condition, description, view):
        self.label = label
        self.condition = condition
        self.description = description
        self.view = view
        self.__class__._registry.append(self)

