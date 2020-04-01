from pathlib import Path
import tempfile
import shutil

import sphinx_rtd_theme


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


def patch_files(path=None, replace_list=None):
    """
    Search and replace content from a list of file based on a pattern
    replace_list[
        {
            'filename_pattern': '*.css',
            'content_patterns': [
                {
                    'search': '',
                    'replace': '',
                }
            ]
        }
    ]
    """
    file_open_mode = 'r+'

    path_object = Path(path)
    for replace_entry in replace_list or []:
        for path_entry in path_object.glob('**/{}'.format(replace_entry['filename_pattern'])):
            if path_entry.is_file():
                for pattern in replace_entry['content_patterns']:
                    with path_entry.open(mode=file_open_mode) as source_file_object:
                        with tempfile.TemporaryFile(mode=file_open_mode) as temporary_file_object:
                            source_position = 0
                            destination_position = 0

                            while(True):
                                source_file_object.seek(source_position)
                                letter = source_file_object.read(1)

                                if len(letter) == 0:
                                    break
                                else:
                                    if letter == pattern['search'][0]:
                                        text = '{}{}'.format(letter, source_file_object.read(len(pattern['search']) - 1))

                                        temporary_file_object.seek(destination_position)
                                        if text == pattern['search']:
                                            text = pattern['replace']
                                            source_position = source_position + len(pattern['search'])
                                            destination_position = destination_position + len(pattern['replace'])
                                            temporary_file_object.write(text)

                                        else:
                                            source_position = source_position + 1
                                            destination_position = destination_position + 1
                                            temporary_file_object.write(letter)
                                    else:
                                        source_position = source_position + 1
                                        destination_position = destination_position + 1
                                        temporary_file_object.write(letter)

                            source_file_object.seek(0)
                            source_file_object.truncate()
                            temporary_file_object.seek(0)
                            shutil.copyfileobj(fsrc=temporary_file_object, fdst=source_file_object)


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
