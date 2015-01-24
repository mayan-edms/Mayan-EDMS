from __future__ import unicode_literals

import os
import sys
import platform
import uuid
import time

from git import Repo
import psutil
import requests
import sh

try:
    from sh import lsb_release, uname
except ImportError:
    LSB = False
else:
    LSB = True


from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.datastructures import SortedDict
from django.conf import settings

from solo.models import SingletonModel

from common.utils import pretty_size
from mayan import __version__ as mayan_version
from lock_manager import Lock, LockError
from ocr.settings import PDFTOTEXT_PATH, TESSERACT_PATH, UNPAPER_PATH

from .classes import PIPNotFound, Property, PropertyNamespace, VirtualEnv
from .literals import FORM_KEY, FORM_RECEIVER_FIELD, FORM_SUBMIT_URL, TIMEOUT


class Installation(SingletonModel):
    _properties = SortedDict()

    is_first_run = models.BooleanField(default=True)
    uuid = models.CharField(max_length=48, blank=True, default=lambda: unicode(uuid.uuid4()))

    def add_property(self, property_instance):
        self._properties[property_instance.name] = property_instance

    def get_properties(self):
        self.set_properties()
        return self._properties.values()

    def os_properties(self):
        namespace = PropertyNamespace('os', _('Operating system'))
        if LSB:
            namespace.add_property('is_lsb', _('LSB OS'), True, True)
            namespace.add_property('distributor_id', _('Distributor ID'), lsb_release('-i', '-s'), True)
            namespace.add_property('description', _('Description'), lsb_release('-d', '-s'), True)
            namespace.add_property('release', _('Release'), lsb_release('-r', '-s'), True)
            namespace.add_property('codename', _('Codename'), lsb_release('-c', '-s'), True)
            namespace.add_property('sysinfo', _('System info'), uname('-a'), True)
        else:
            namespace.add_property('is_lsb', _('LSB OS'), False)

        namespace.add_property('architecture', _('OS architecture'), platform.architecture(), report=True)
        namespace.add_property('python_version', _('Python version'), platform.python_version(), report=True)
        namespace.add_property('hostname', _('Hostname'), platform.node())
        namespace.add_property('platform', _('Platform'), sys.platform, report=True)
        namespace.add_property('machine', _('Machine'), platform.machine(), report=True)
        namespace.add_property('processor', _('Processor'), platform.processor(), report=True)
        namespace.add_property('cpus', _('Number of CPUs'), psutil.cpu_count(), report=True)
        namespace.add_property('total_phymem', _('Total physical memory'), pretty_size(psutil.virtual_memory().total), report=True)
        namespace.add_property('disk_partitions', _('Disk partitions'), '; '.join(['%s %s %s %s' % (partition.device, partition.mountpoint, partition.fstype, partition.opts) for partition in psutil.disk_partitions()]))

    def binary_dependencies(self):
        namespace = PropertyNamespace('bins', _('Binary dependencies'))

        try:
            tesseract = sh.Command(TESSERACT_PATH)
        except sh.CommandNotFound:
            namespace.add_property('tesseract', _('tesseract version'), _('not found'), report=True)
        except Exception:
            namespace.add_property('tesseract', _('tesseract version'), _('error getting version'), report=True)
        else:
            namespace.add_property('tesseract', _('tesseract version'), tesseract('-v').stderr, report=True)

        try:
            unpaper = sh.Command(UNPAPER_PATH)
        except sh.CommandNotFound:
            namespace.add_property('unpaper', _('unpaper version'), _('not found'), report=True)
        except Exception:
            namespace.add_property('unpaper', _('unpaper version'), _('error getting version'), report=True)
        else:
            namespace.add_property('unpaper', _('unpaper version'), unpaper('-V').stdout, report=True)

        try:
            pdftotext = sh.Command(PDFTOTEXT_PATH)
        except sh.CommandNotFound:
            namespace.add_property('pdftotext', _('pdftotext version'), _('not found'), report=True)
        except Exception:
            namespace.add_property('pdftotext', _('pdftotext version'), _('error getting version'), report=True)
        else:
            namespace.add_property('pdftotext', _('pdftotext version'), pdftotext('-v').stderr, report=True)

    def mayan_properties(self):
        namespace = PropertyNamespace('mayan', _('Mayan EDMS'))

        namespace.add_property('uuid', _('UUID'), self.uuid, report=True)
        namespace.add_property('mayan_version', _('Mayan EDMS version'), mayan_version, report=True)

    def git_properties(self):
        namespace = PropertyNamespace('git', _('Git repository'))

        try:
            repo = Repo(os.path.abspath(settings.BASE_DIR))
        except:
            namespace.add_property('is_git_repo', _('Running from a Git repository'), False)
        else:
            try:
                repo.config_reader()
                headcommit = repo.active_branch.commit
                namespace.add_property('is_git_repo', _('Running from a Git repository'), True)
                namespace.add_property('repo_remotes', _('Repository remotes'), ', '.join([unicode(remote) for remote in repo.remotes]), report=True)
                namespace.add_property('repo_remotes_urls', _('Repository remotes URLs'), ', '.join([unicode(remote.url) for remote in repo.remotes]), report=True)
                namespace.add_property('repo_head_reference', _('Branch'), repo.head.reference, report=True)
                namespace.add_property('headcommit_hexsha', _('HEAD commit hex SHA'), headcommit.hexsha, report=True)
                namespace.add_property('headcommit_author', _('HEAD commit author'), headcommit.author)
                namespace.add_property('headcommit_authored_date', _('HEAD commit authored date'), time.asctime(time.gmtime(headcommit.authored_date)), report=True)
                namespace.add_property('headcommit_committer', _('HEAD commit committer'), headcommit.committer)
                namespace.add_property('headcommit_committed_date', _('HEAD commit committed date'), time.asctime(time.gmtime(headcommit.committed_date)), report=True)
                namespace.add_property('headcommit_message', _('HEAD commit message'), headcommit.message, report=True)
            except:
                # Error getting git information, leave blank
                pass

    def virtualenv_properties(self):
        namespace = PropertyNamespace('venv', _('VirtualEnv'))
        try:
            venv = VirtualEnv()
        except PIPNotFound:
            namespace.add_property('pip', 'pip', _('pip not found.'), report=True)
        else:
            for item, version, result in venv.get_results():
                namespace.add_property(item, '%s (%s)' % (item, version), result, report=True)

    def set_properties(self):
        self._properties = SortedDict()
        self.os_properties()
        self.binary_dependencies()
        self.mayan_properties()
        self.git_properties()
        self.virtualenv_properties()

    def __getattr__(self, name):
        self.set_properties()
        try:
            return self._properties[name].value
        except KeyError:
            raise AttributeError

    def submit(self):
        try:
            lock = Lock.acquire_lock('upload_stats')
        except LockError:
            pass
        else:
            self.set_properties()

            try:
                requests.post(FORM_SUBMIT_URL, data={'formkey': FORM_KEY, FORM_RECEIVER_FIELD: Property.get_reportable(as_json=True)}, timeout=TIMEOUT)
            except Exception:
                raise
            else:
                self.is_first_run = False
                self.save()
            finally:
                lock.release()

    class Meta:
        verbose_name = verbose_name_plural = _('Installation details')
