import sys
import platform
import uuid

import pbs
import psutil
import requests

try:
    from pbs import lsb_release, uname
except pbs.CommandNotFound:
    LSB = False
else:
    LSB = True

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.datastructures import SortedDict
from django.utils.simplejson import dumps

from common.models import Singleton
from common.utils import pretty_size

FORM_SUBMIT_URL = 'https://docs.google.com/spreadsheet/formResponse'
FORM_KEY = 'dGZrYkw3SDl5OENMTG15emp1UFFEUWc6MQ'
FORM_RECEIVER_FIELD = 'entry.0.single'
TIMEOUT = 5


class Property(object):
    def __init__(self, name, label, value):
        self.name = name
        self.label = label
        self.value = value
        
    def __unicode__(self):
        return unicode(self.value)

    def __str__(self):
        return str(self.value)
        

class Installation(Singleton):
    _properties = SortedDict()

    is_first_run = models.BooleanField(default=False)
    uuid = models.CharField(max_length=48, blank=True, default=lambda: unicode(uuid.uuid4()))

    def add_property(self, property_instance):
        self._properties[property_instance.name] = property_instance

    def get_properties(self):
        self.set_properties()
        return self._properties

    def set_properties(self):
        self._properties = SortedDict()
        if LSB:
            self.add_property(Property('is_lsb', _(u'LSB OS'), True))
            self.add_property(Property('distributor_id', _(u'Distributor ID'), lsb_release('-i','-s')))
            self.add_property(Property('description', _(u'Description'), lsb_release('-d','-s')))
            self.add_property(Property('release', _(u'Release'), lsb_release('-r','-s')))
            self.add_property(Property('codename', _(u'Codename'), lsb_release('-c','-s')))
            self.add_property(Property('sysinfo', _(u'System info'), uname('-a')))
        else:
            self.add_property(Property('is_posix', _(u'POSIX OS'), False))

        self.add_property(Property('architecture', _(u'OS architecture'), platform.architecture()))
        self.add_property(Property('python_version', _(u'Python version'), platform.python_version()))
        self.add_property(Property('hostname', _(u'Hostname'), platform.node()))
        self.add_property(Property('platform', _(u'Platform'), sys.platform))
        self.add_property(Property('machine', _(u'Machine'), platform.machine()))
        self.add_property(Property('processor', _(u'Processor'), platform.processor()))
        self.add_property(Property('cpus', _(u'Number of CPUs'), psutil.NUM_CPUS))
        self.add_property(Property('total_phymem', _(u'Total physical memory'), pretty_size(psutil.TOTAL_PHYMEM)))
        self.add_property(Property('disk_partitions', _(u'Disk partitions'), '; '.join(['%s %s %s %s' % (partition.device, partition.mountpoint, partition.fstype, partition.opts) for partition in psutil.disk_partitions()])))
        
        try:
            self.add_property(Property('tesseract', _(u'tesseract version'), pbs.tesseract('-v').stderr))
        except pbs.CommandNotFound:
            self.add_property(Property('tesseract', _(u'tesseract version'), _(u'not found')))

        try:
            self.add_property(Property('unpaper', _(u'unpaper version'), pbs.unpaper('-V').stdout))
        except pbs.CommandNotFound:
            self.add_property(Property('unpaper', _(u'unpaper version'), _(u'not found')))
            
    def __getattr__(self, name):
        self.set_properties()
        try:
            return self._properties[name]
        except KeyError:
            raise AttributeError, name

    def submit(self):
        try:
            dictionary = {}
            if self.is_lsb:
                dictionary.update(
                    {
                        'is_lsb': unicode(self.is_lsb),
                        'distributor_id': unicode(self.distributor_id),
                        'description': unicode(self.description),
                        'release': unicode(self.release),
                        'codename': unicode(self.codename),
                        'sysinfo': unicode(self.sysinfo),
                    }
                )

            dictionary.update(
                {
                    'uuid': self.uuid,
                    'architecture': unicode(self.architecture),
                    'python_version': unicode(self.python_version),
                    'platform': unicode(self.platform),
                    'machine': unicode(self.machine),
                    'processor': unicode(self.processor),
                    'cpus': unicode(self.cpus),
                    'total_phymem': unicode(self.total_phymem),
                }
            )
            
            requests.post(FORM_SUBMIT_URL, data={'formkey': FORM_KEY, FORM_RECEIVER_FIELD: dumps(dictionary)}, timeout=TIMEOUT)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            pass
        else:
            self.is_first_run = False
            self.save()

    class Meta:
        verbose_name = verbose_name_plural = _(u'installation details')
