from __future__ import absolute_import

import os
import tempfile

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import management

from .literals import FIXTURE_TYPES_CHOICES, FIXTURE_FILE_TYPE


class BootstrapSetup(models.Model):
    """
    Model to store the fixture for a pre configured setup
    """
    name = models.CharField(max_length=128, verbose_name=_(u'name'), unique=True)
    description = models.TextField(verbose_name=_(u'description'), blank=True)
    fixture = models.TextField(verbose_name=_(u'fixture'))
    type = models.CharField(max_length=16, verbose_name=_(u'type'), choices=FIXTURE_TYPES_CHOICES)

    def __unicode__(self):
        return self.name

    def get_extension(self):
        return FIXTURE_FILE_TYPE[self.type]

    def execute(self):
        handle, filepath = tempfile.mkstemp()
        # Just need the filepath, close the file description
        os.close(handle)

        filepath = os.path.extsep.join([filepath, self.get_extension()])

        with open(filepath, 'w') as file_handle:
            file_handle.write(self.fixture)

        management.call_command('loaddata', filepath, verbosity=0)
        os.unlink(filepath)

    class Meta:
        verbose_name = _(u'bootstrap setup')
        verbose_name_plural = _(u'bootstrap setups')
