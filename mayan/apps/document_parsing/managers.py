from __future__ import unicode_literals

from datetime import timedelta
import logging

from django.apps import apps
from django.db import models
from django.utils.timezone import now

logger = logging.getLogger(__name__)


class DocumentPageContentManager(models.Manager):
    pass
