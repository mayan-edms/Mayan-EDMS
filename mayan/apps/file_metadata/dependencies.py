from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.dependencies.classes import BinaryDependency

from .drivers.exiftool import EXIFToolDriver

exiftool = EXIFToolDriver(auto_initialize=False)
exiftool.read_settings()

BinaryDependency(
    help_text=_(
        'Library and program to read and write meta information in multimedia '
        'files.'
    ), module=__name__, name='exiftool', path=exiftool.exiftool_path
)
