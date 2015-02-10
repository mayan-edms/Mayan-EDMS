from __future__ import unicode_literals

from json import dumps, loads
import requests

from django.db import models
from django.utils.translation import ugettext_lazy as _

from solo.models import SingletonModel

from installation.models import Installation
from lock_manager import Lock, LockError

from .literals import FORM_KEY, FORM_RECEIVER_FIELD, FORM_SUBMIT_URL, TIMEOUT
from .exceptions import AlreadyRegistered


class RegistrationSingleton(SingletonModel):
    _cached_name = None
    _registered = None

    registered = models.BooleanField(default=False, verbose_name=_('Registered'))
    registration_data = models.TextField(verbose_name=_('Registration data'), blank=True)

    @classmethod
    def registration_state(cls):
        if cls._registered:
            return cls._registered
        else:
            instance = cls.objects.get()
            if instance.is_registered:
                cls._registered = instance.is_registered
            return instance.is_registered

    @classmethod
    def registered_name(cls):
        if cls._cached_name:
            return cls._cached_name
        else:
            instance = cls.objects.get()
            try:
                dictionary = loads(instance.registration_data)
            except ValueError:
                dictionary = {}
            name_value = dictionary.get('company') or dictionary.get('name')
            if name_value:
                cls._cached_name = name_value

            return name_value or _('No name')

    @property
    def is_registered(self):
        return self.registered

    def register(self, form_data):
        if self.is_registered:
            raise AlreadyRegistered

        installation = Installation.objects.get()
        dictionary = {}
        dictionary.update(form_data)
        dictionary.update({
            'uuid': installation.uuid
        })
        self.registration_data = dumps(dictionary)
        self.save()
        self.submit()

    def submit(self):
        try:
            lock = Lock.acquire_lock('upload_registration')
        except LockError:
            pass
        else:
            try:
                requests.post(FORM_SUBMIT_URL, data={'formkey': FORM_KEY, FORM_RECEIVER_FIELD: self.registration_data}, timeout=TIMEOUT)
            except Exception:
                raise
            else:
                self.registered = True
                self.save()
            finally:
                lock.release()

    class Meta:
        verbose_name = verbose_name_plural = _('Registration properties')
