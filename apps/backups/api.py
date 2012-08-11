from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.core.management.commands.dumpdata import Command
from django.db import router, DEFAULT_DB_ALIAS


class ElementBackupBase(object):
    """
    Sub classes must provide at least:
        info()
        backup()
        restore()
    """

    label = _(u'Base backup manager')

    def info(self):
        """
        Must return at least None
        """
        return None

    def link(self, app_backup):
        self.app_backup = app_backup
        return self

    def __unicode__(self):
        return unicode(self.__class__.label)


class ElementBackupModel(ElementBackupBase):
    label = _(u'Model fixtures')

    def __init__(self, models=None):
        self.model_list = models or []
    
    def info(self):
        return _(u'models: %s') % (u', '.join(self.model_list) if self.model_list else _(u'All'))

    def backup(self):
        """
        TODO: turn into a generator maybe?
        """
        command = Command()
        if not self.model_list:
            result = [self.app_backup.name]
        else:
            result = [u'%s.%s' (self.app_backup.name, model) for model in self.model_list]
        result = command.handle(u' '.join(result), format='json', indent=4, using=DEFAULT_DB_ALIAS, exclude=[], user_base_manager=False, use_natural_keys=False)
        return result


class ElementBackupFile(ElementBackupBase):
    label = _(u'File copy')

    def __init__(self, storage_class, filepath=None):
        self.storage_class = storage_class
        self.filepath = filepath
    
    def info(self):
        return _(u'%s from %s') % (self.filepath or _(u'all files'), self.storage_class)

    def backup(self):
        """
        Fetch a file specified by filepath from the Django storage class
        and return a file like object
        """
        return None
        

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
        self.backup_managers = [manager.link(self) for manager in backup_managers]
        self.state = self.__class__.STATE_IDLE
        self.__class__._registry[name] = self

    def info(self):
        results = []
        for manager in self.backup_managers:
            results.append(u'%s - %s' % (manager, manager.info() or _(u'Nothing')))
        return u', '.join(results)

    def backup(self, storage_module, *args, **kwargs):
        self.state = self.__class__.STATE_BACKING_UP
        for manager in self.backup_managers:
            result = manager.backup()
            storage_module.backup(result)
        self.state = self.__class__.STATE_IDLE

    def restore(self, storage_module=None):
        self.state = self.__class__.STATE_RESTORING
        for manager in self.backup_managers:
            manager.restore(storage_module.restore())
        self.state = self.__class__.STATE_IDLE

    def __unicode__(self):
        return unicode(self.label)


class StorageModuleBase(object):
    #_registry = {}
    _registry = []
    
    REALM_LOCAL = 'local'
    REALM_REMOTE = 'remote'
    
    REALM_CHOICES = (
        (REALM_LOCAL, _(u'local')),
        (REALM_REMOTE, _(u'remote')),
    )
    
    # TODO: register subclasses of StorageModuleBase
    # do not register instances
    #def __new__(cls, *args, **kwargs):
    #    print "NEW"

    @classmethod
    def register(cls, klass):
        cls._registry.append(klass)

    def __init__(self, *args, **kwargs):
        pass
       
    def backup(self, data):
        raise NotImplemented
        
    def restore(self):
        """
        Must return data or a file like object
        """
        raise NotImplemented


class TestStorageModule(StorageModuleBase):
    label = _(u'Test storage module')

    def __init__(self, *args, **kwargs):
        self.backup_path = kwargs.pop('backup_path', None)
        self.restore_path = kwargs.pop('restore_path', None)
        return super(TestStorageModule, self).__init__(*args, **kwargs)
    
    def backup(self, data):
        print '***** received data'
        print data 
        print '***** saving to path: %s' % self.backup_path
    
    def restore(self):
        print 'restore from path: %s' % self.restore_path
        return 'sample_data'

# TODO: get rid of register and try to register on subclassing
StorageModuleBase.register(TestStorageModule)
