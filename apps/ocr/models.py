from __future__ import absolute_import

from ast import literal_eval
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.exceptions import ValidationError

from common.models import Singleton
from documents.models import Document, DocumentVersion
from converter.api import get_available_transformations_choices
from sources.managers import SourceTransformationManager

from .literals import (OCR_STATE_CHOICES, OCR_STATE_ENABLED,
    OCR_STATE_DISABLED)
from .managers import OCRProcessingManager
from .exceptions import (ReQueueError, OCRProcessingAlreadyDisabled,
    OCRProcessingAlreadyEnabled)


class OCRProcessingSingleton(Singleton):
    state = models.CharField(max_length=4,
        choices=OCR_STATE_CHOICES,
        default=OCR_STATE_ENABLED,
        verbose_name=_(u'state'))

    #objects = AnonymousUserSingletonManager()

    def __unicode__(self):
        return ugettext('OCR processing')

    def disable(self):
        if self.state == OCR_STATE_DISABLED:
            raise OCRProcessingAlreadyDisabled
        
        self.state = OCR_STATE_DISABLED
        self.save()

    def enable(self):
        if self.state == OCR_STATE_ENABLED:
            raise OCRProcessingAlreadyEnabled
        
        self.state = OCR_STATE_ENABLED
        self.save()
        
    def is_enabled(self):
        return self.state == OCR_STATE_ENABLED

    class Meta:
        verbose_name = verbose_name_plural = _(u'OCR processing properties')
