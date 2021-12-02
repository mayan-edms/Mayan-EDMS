#!/usr/bin/env python

import optparse
import os
from pathlib import Path
import sys

from docutils import core
from html2bbcode.parser import HTML2BBCode
from lxml import etree, html
import sh

import django
from django.conf import settings

MONTHS_TO_NUMBER = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}
VERSION = '3.0'
ignore_ids_list = ('upgrade-process', 'troubleshooting')


class ReleaseNoteExporter:
    @staticmethod
    def filter_elements(tree):
        result = []

        for element in tree:
            if element.attrib.get('id') not in ignore_ids_list:

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

    def __init__(self):
        sys.path.insert(0, os.path.abspath('..'))
        sys.path.insert(1, os.path.abspath('.'))

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mayan.settings')

        self.parser = optparse.OptionParser(
            usage='%prog [version number]', version='%prog {}'.format(VERSION)
        )
        self.parser.add_option(
            '-f', '--format', help='specify the output format',
            dest='output_format',
            action='store', metavar='output_format'
        )

        (self.options, args) = self.parser.parse_args()

        if len(args) != 1:
            self.parser.error('version argument is missing')

        django.setup()

        self.version = args[0]

    def export(self):
        path_documentation = Path(
            settings.BASE_DIR
        ) / '..' / 'docs' / 'releases' / '{}.txt'.format(self.version)

        with path_documentation.open(mode='r') as file_object:
            content = []

            for line in file_object:
                if line.startswith('.. include'):
                    # Skip
                    pass
                elif ':gitlab-issue:' in line:
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

        if self.options.output_format == 'bb':
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
        elif self.options.output_format == 'md':
            command_pandoc = sh.Command('pandoc')

            markdown_tag_cleanup = (
                (b'class="docutils literal"', b''),
                (b'class="reference external"', b''),
            )

            joined_result = b''.join(result)

            for markdown_tag_cleanup_item in markdown_tag_cleanup:
                joined_result = joined_result.replace(*markdown_tag_cleanup_item)

            return command_pandoc(_in=joined_result, f='html', t='markdown')
        elif self.options.output_format == 'news':
            command_pandoc = sh.Command('pandoc')

            markdown_tag_cleanup = (
                (b'class="docutils literal"', b''),
                (b'class="reference external"', b''),
            )

            joined_result = b''.join(result)

            for markdown_tag_cleanup_item in markdown_tag_cleanup:
                joined_result = joined_result.replace(*markdown_tag_cleanup_item)

            result_body = command_pandoc(_in=joined_result, f='html', t='markdown')

            tree = html.fromstring(html_fragment)
            # ~ title = tree[0].text
            # ~ date tree[1].text)

            released, month, day, year = tree[1].text.split(' ')

            return '\n'.join(
                (
                    '---',
                    'date: {}-{:02d}-{:02d}'.format(year, MONTHS_TO_NUMBER[month], int(day[:-1])),
                    'title: "{}"'.format(tree[0].text),
                    '---',
                    str(result_body)
                )
            )
        else:
            return b''.join(result)


if __name__ == '__main__':
    message_processor = ReleaseNoteExporter()
    result = message_processor.export()
    print(result)
