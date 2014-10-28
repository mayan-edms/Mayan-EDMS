from __future__ import absolute_import

from . import setup_link

setup_items = []


def register_setup(link):
    setup_items.append(link)
