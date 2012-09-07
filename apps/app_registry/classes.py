import logging
import os

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.management.commands.dumpdata import Command
from django.conf import settings
from django.db import router, DEFAULT_DB_ALIAS
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.importlib import import_module

logger = logging.getLogger(__name__)


# Data types
class ElementDataBase(object):
    """
    The basic unit of a backup, a data type
    it is produced or consumed by the ElementBackup classes
    """
    def make_filename(self, id):
        return '%s-%s' % (self.model_backup.app_backup.app.name, id)
    
    def save(self):
        """
        Must return a file like object
        """
        raise NotImplemented

    def load(self, file_object):
        """
        Must read a file like object and store content
        """
        raise NotImplemented        


class Fixture(ElementDataBase):
    name = 'fixture'
    
    def __init__(self, model_backup, content):
        self.model_backup = model_backup
        self.content = content
    
    @property
    def filename(self):
        return self.make_filename(self.__class__.name)
    
    def save(self):
        return ContentFile(name=self.filename, content=self.content)

    #def load(self):


# Element backup
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


class ModelBackup(ElementBackupBase):
    label = _(u'Model fixtures')

    def __init__(self, models=None):
        self.model_list = models or []
    
    def info(self):
        return _(u'models: %s') % (u', '.join(self.model_list) if self.model_list else _(u'All'))

    def backup(self):
        """
        """
        #TODO: turn into a generator

        command = Command()
        if not self.model_list:
            result = [self.app_backup.app.name]
        else:
            result = [u'%s.%s' (self.app_backup.app.name, model) for model in self.model_list]
        
        #TODO: a single Fixture or a list of Fixtures for each model?
        #Can't return multiple Fixture until a way to find all of an app's models is found
        return [Fixture(
            model_backup=self,
            content=command.handle(u' '.join(result), format='json', indent=4, using=DEFAULT_DB_ALIAS, exclude=[], user_base_manager=False, use_natural_keys=False)
        )]


class FileBackup(ElementBackupBase):
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
        

# App config
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

    def __init__(self, app, backup_managers):
        # app = App instance from app_registry app
        self.app = app
        self.backup_managers = [manager.link(self) for manager in backup_managers]
        self.state = self.__class__.STATE_IDLE
        self.__class__._registry[app] = self

    def info(self):
        results = []
        for manager in self.backup_managers:
            results.append(u'%s - %s' % (manager, manager.info() or _(u'Nothing')))
        return u', '.join(results)


