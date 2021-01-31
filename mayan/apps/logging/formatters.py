import logging

from django.utils.termcolors import colorize

from .literals import FORMATTER_PALETTE


class ColorFormatter(logging.Formatter):
    def format(self, record):
        record.msg = colorize(
            text=record.msg, **FORMATTER_PALETTE.get(record.levelname, {})
        )
        return super().format(record)
