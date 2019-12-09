from __future__ import unicode_literals

import shutil

from pathlib2 import Path
import sphinx_rtd_theme

from mayan.apps.storage.utils import patch_files


def load_env_file(filename='../config.env'):
    result = {}
    with open(filename) as file_object:
        for line in file_object:
            if not line.startswith('#'):
                key, value = line.strip().split('=')
                result[key] = value

    return result


def generate_substitutions(dictionary):
    result = []

    for key, value in dictionary.items():
        result.append(('|{}|'.format(key), value))

    return result


def patch_theme_template(app, templates_path):
    package_path = Path(sphinx_rtd_theme.__file__)
    template_files = ('footer.html', 'layout.html',)
    replace_list=[
        {
            'filename_pattern': 'footer.html',
            'content_patterns': [
                {
                    'search': '{{ _(\'Next\') }}',
                    'replace': '{{ next.title }}',
                },
                {
                    'search': '{{ _(\'Previous\') }}',
                    'replace': '{{ prev.title }}',
                },
            ]
        },
        {
            'filename_pattern': 'layout.html',
            'content_patterns': [
                {
                    'search': '</div>\n    </nav>\n\n    <section data-toggle="wy-nav-shift" class="wy-nav-content-wrap">',
                    'replace': '{% include "message_area.html" %}</div>\n    </nav>\n\n    <section data-toggle="wy-nav-shift" class="wy-nav-content-wrap">',
                },
            ]
        }
    ]

    for template_file in template_files:
        source_file_path = package_path.parent / template_file#'layout.html'
        destination_path = Path(app.srcdir) / templates_path
        destination_file_path = destination_path / template_file#'layout.html'

        with source_file_path.open(mode='r') as source_file_object:
            with destination_file_path.open(mode='w+') as destination_file_object:
                shutil.copyfileobj(
                    fsrc=source_file_object, fdst=destination_file_object
                )


    patch_files(
        path=destination_path, replace_list=replace_list
    )
