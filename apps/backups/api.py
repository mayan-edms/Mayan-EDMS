from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext


class BackupManagerBase(object):
    label = _(u'Base backup manager')
    #def __init__(self, name, label):
    #    self.label = label
    #    self.name = name

    def info(self):
        return None

    def __unicode__(self):
        return unicode(self.__class__.label)


class ModelFixtures(BackupManagerBase):
    label = _(u'Model fixtures')

    def __init__(self, models=None):
        self.model_list = models or []
    
    def info(self):
        return u', '.join(self.model_list) or _(u'All')


class DirectoryCopy(BackupManagerBase):
    label = _(u'Directory copy')

    def __init__(self, path):
        self.path = path
    
    def info(self):
        return self.path


class AppBackup(object):
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

    def __init__(self, name, label, backup_managers):
        self.label = label
        self.name = name
        self.backup_managers = backup_managers
        self.state = self.__class__.STATE_IDLE
        self.__class__._registry[name] = self

    @property
    def info(self):
        results = []
        for manager in self.backup_managers:
            results.append(u'%s - %s' % (manager, manager.info() or _(u'Nothing')))
        return u', '.join(results)

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


class StorageModuleBase(object):
    _registry = {}

    def __init__(self, name, label):
        self.label = label
        self.name = name
        self.__class__._registry[name] = self
        
    def backup(self, *args, **kwargs):
        raise NotImplemented
        
    def restore(self, *args, **kwargs):
        raise NotImplemented
