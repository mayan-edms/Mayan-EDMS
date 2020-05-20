#!/usr/bin/env python

import os
from pathlib import Path
import sys

from docutils import core
from html2bbcode.parser import HTML2BBCode
from lxml import etree, html

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(1, os.path.abspath('.'))

from mayan.settings import BASE_DIR

ignore_ids_list = ('upgrading-process',)


class ReleaseNoteExporter(object):
    @staticmethod
    def filter_elements(tree):
        result = []

        for element in tree:
            if element.tag == 'div':
                if not element.attrib.get('id') in ignore_ids_list:
                    result.extend(
                        ReleaseNoteExporter.filter_elements(tree=element)
                    )
            else:
                if not element.attrib.get('id') in ignore_ids_list:
                    result.append(
                        etree.tostring(element).replace(b'\n', b' ')
                    )

        return result

    def __init__(self, version):
        self.version = version

    def export(self):
        path_documentation = Path(
            BASE_DIR
        ) / '..' / 'docs' / 'releases' / '{}.txt'.format(self.version)

        with path_documentation.open(mode='r') as file_object:
            content = []

            content.append('New version of Mayan EDMS available\n')
            content.append('===================================\n\n\n\n\n\n')

            content.append(
                'Please read the release notes before upgrading: '
                'https://docs.mayan-edms.com/releases/{}.html\n\n'.format(
                    self.version
                )
            )

            content.append('Package locations\n')
            content.append('=================\n\n\n\n\n\n\n\n')

            content.append(
                'Docker image available at: '
                'https://hub.docker.com/r/mayanedms/mayanedms\n\n'
            )
            content.append(
                'Python packages available at: '
                'https://pypi.org/project/mayan-edms/{}/ and '
                'installed via:\n\n'.format(self.version)
            )

            content.append(
                '``pip install mayan-edms=={}``\n\n'.format(self.version)
            )
            file_object.readline()
            file_object.readline()
            file_object.readline()
            file_object.readline()
            for line in file_object:
                if ':gitlab-issue:' in line:
                    line_parts = line.split('`')

                    result = (
                        '- `GitLab issue #{} '
                        '<https://gitlab.com/mayan-edms/mayan-edms/issues/{}>`_ {}'.format(
                            line_parts[1], line_parts[1], line_parts[2]
                        )
                    )

                    content.append(result)
                else:
                    content.append(line)

        parts = core.publish_parts(
            source=''.join(content), writer_name='html'
        )
        html_fragment = '{}{}'.format(
            parts['body_pre_docinfo'], parts['fragment']
        )

        result = ReleaseNoteExporter.filter_elements(
            tree=html.fromstring(html_fragment)
        )

        result = result[1:]
        html_output = str(b''.join(result))

        html_replace_list = (
            ('<tt', '<code'),
            ('</tt>', '</code>'),
        )

        for html_replace_item in html_replace_list:
            html_output = html_output.replace(*html_replace_item)

        parser = HTML2BBCode()

        result = str(parser.feed(html_output))

        bbcode_replace_list = (
            ('[h1]', '\n[size=150]'),
            ('[/h1]', '[/size]\n'),
            ('[h2]', '\n[size=150]'),
            ('[/h2]', '[/size]\n'),
            ('[h3]', '\n[b]'),
            ('[/h3]', '[/b]\n'),
            ('[li]', '\n[*]'),
            ('[/li]', ''),
            ('[code]', '[b][i]'),
            ('[/code]', '[/i][/b]'),
        )

        for bbcode_replace_item in bbcode_replace_list:
            result = result.replace(*bbcode_replace_item)

        return result


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(
            'usage: export_release_notes <version>'
        )
        exit(0)

    print(
        ReleaseNoteExporter(version=sys.argv[1]).export()
    )
