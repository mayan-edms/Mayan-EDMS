from django.utils.translation import ugettext_lazy as _


class MetadataClass(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def __getattr__(self, name):
        if name in self.dictionary:
            return self.dictionary.get(name)
        else:
            raise AttributeError(_(u'\'metadata\' object has no attribute \'%s\'') % name)
