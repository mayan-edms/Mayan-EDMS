from __future__ import absolute_import

from elementtree.ElementTree import SubElement

from . import setup_menu


def register_setup(link):
    SubElement(setup_menu, 'setup_link', link=link)
