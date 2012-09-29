from __future__ import absolute_import

import os
import tempfile

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import management

from .literals import (FIXTURE_TYPES_CHOICES, FIXTURE_FILE_TYPE, COMMAND_LOADDATA)
from .managers import BootstrapSetupManager
from .classes import BootstrapModel


class BootstrapSetup(models.Model):
    """
    Model to store the fixture for a pre configured setup.
    """
    name = models.CharField(max_length=128, verbose_name=_(u'name'), unique=True)
    description = models.TextField(verbose_name=_(u'description'), blank=True)
    fixture = models.TextField(verbose_name=_(u'fixture'), help_text=_(u'These are the actual database structure creation instructions.'))
    type = models.CharField(max_length=16, verbose_name=_(u'type'), choices=FIXTURE_TYPES_CHOICES)

    objects = BootstrapSetupManager()

    def __unicode__(self):
        return self.name

    def get_extension(self):
        return FIXTURE_FILE_TYPE[self.type]

    def execute(self):
        BootstrapModel.check_for_data()
        handle, filepath = tempfile.mkstemp()
        # Just need the filepath, close the file description
        os.close(handle)

        filepath = os.path.extsep.join([filepath, self.get_extension()])

        with open(filepath, 'w') as file_handle:
            file_handle.write(self.fixture)

        management.call_command(COMMAND_LOADDATA, filepath, verbosity=0)
        os.unlink(filepath)

    def compress(self):
        """
        Return a compacted and compressed version of the BootstrapSetup
        instance, meant for download.
        """
        return ''

    def save(self, *args, **kwargs):
        return super(BootstrapSetup, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'bootstrap setup')
        verbose_name_plural = _(u'bootstrap setups')
        ordering = ['name']
