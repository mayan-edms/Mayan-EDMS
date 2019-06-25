from __future__ import unicode_literals

import io

from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from mayan.apps.converter.models import Transformation


class Redaction(Transformation):
    class Meta:
        proxy = True
