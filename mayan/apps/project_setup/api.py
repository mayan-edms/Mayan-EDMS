from __future__ import absolute_import

from . import setup_link

setup_items = []


def register_setup(link):
    setup_items.append(link)

    # Append the link's children_view_regex to the setup main menu children view regex
    setup_link.setdefault('children_view_regex', [])
    setup_link['children_view_regex'].extend(link.get('children_view_regex', []))
