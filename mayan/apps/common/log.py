from __future__ import unicode_literals

import logging

from django.utils.termcolors import colorize

PALETTE = {
    'CRITICAL': {'fg': 'red', 'opts': ('bold', 'blink', 'reverse')},
    'DEBUG': {'fg': 'cyan'},
    'ERROR': {'fg': 'red', 'opts': ('bold',)},
    'INFO': {'fg': 'white'},
    'SUCCESS': {'fg': 'green'},
    'WARNING': {'fg': 'yellow', 'opts': ('bold', 'underscore')},
}


class ColorFormatter(logging.Formatter):
    def format(self, record):
        record.msg = colorize(
            text=record.msg, **PALETTE.get(record.levelname, {})
        )
        return super(ColorFormatter, self).format(record)
