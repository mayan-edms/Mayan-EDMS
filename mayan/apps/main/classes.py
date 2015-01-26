class FrontPageButton(object):
    _registry = []

    @classmethod
    def get_all(cls):
        return cls._registry

    def __init__(self, link):
        self.link = link
        self.__class__._registry.append(link)
