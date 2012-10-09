from __future__ import absolute_import

import requests

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.simplejson import dumps, loads

from common.models import Singleton
from lock_manager import Lock, LockError

from .literals import FORM_SUBMIT_URL, FORM_KEY, FORM_RECEIVER_FIELD, TIMEOUT
from .exceptions import AlreadyRegistered


class RegistrationSingleton(Singleton):
    _cached_name = None
    _registered = None

    registered = models.BooleanField(default=False, verbose_name=_('registered'))
    registration_data = models.TextField(verbose_name=_(u'registration data'), blank=True)

    @classmethod
    def purge_cache(cls):
        cls._cached_name = None
        cls._registered = None

    @classmethod
    def registration_state(cls):
        if cls._registered:
            return cls._registered
        else:
            instance = cls.objects.get()
            cls._registered = instance.is_registered
            return cls._registered

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
            company = dictionary.get('company')
            name = dictionary.get('name')
            cls._cached_name = company or name or _(u'No name')
        
            return cls._cached_name

    @property
    def is_registered(self):
        return self.registered

    def register(self, form):
        from installation.models import Installation

        #if self.is_registered:
        #    raise AlreadyRegistered

        installation = Installation.objects.get()
        dictionary = {}
        dictionary.update(form.cleaned_data)
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
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                pass
            else:
                self.registered = True
                self.__class__.purge_cache()
                self.save()
            finally:
                lock.release()

    class Meta:
        verbose_name = verbose_name_plural = _(u'registration properties')
