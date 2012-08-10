from django.utils.translation import ugettext_lazy as _


class ModuleBackup(object):
    _registry = {}
 
    STATE_BACKING_UP = 'backing_up'
    STATE_RESTORING = 'restoring'
    STATE_IDLE = 'idle'
    
    STATE_CHOICES = (
        (STATE_BACKING_UP, _(u'backing up')),
        (STATE_RESTORING, _(u'restoring')),
        (STATE_IDLE, _(u'idle')),
    )

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_all(cls):
        return cls._registry.values()

    def __init__(self, name, label):
        self.label = label
        self.name = name
        self.state = self.__class__.STATE_IDLE
        self.__class__._registry[name] = self

    def backup(self, storage_module=None):
        self.state = self.__class__.STATE_BACKING_UP
        # call storage_module
        self.state = self.__class__.STATE_IDLE

    def restore(self, storage_module=None):
        self.state = self.__class__.STATE_RESTORING
        # call storage_module
        self.state = self.__class__.STATE_IDLE

    def __unicode__(self):
        return unicode(self.label)
