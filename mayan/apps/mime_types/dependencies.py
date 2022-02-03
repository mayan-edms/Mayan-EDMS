from django.utils.translation import ugettext_lazy as _

from mayan.apps.dependencies.classes import BinaryDependency, PythonDependency

from .backends.literals import DEFAULT_FILE_PATH, DEFAULT_MIMETYPE_PATH


BinaryDependency(
    label='File::MimeInfo', help_text=_(
        'This module can be used to determine the MIME type of a file. '
        'It tries to implement the freedesktop specification for a shared '
        'MIME database.'
    ), module=__name__, name='libfile-mimeinfo-perl',
    path=DEFAULT_MIMETYPE_PATH
)
BinaryDependency(
    label='file', help_text=_('determine file type using content tests'),
    module=__name__, name='file', path=DEFAULT_FILE_PATH
)
PythonDependency(
    copyright_text='''
        The MIT License (MIT)

        Copyright (c) 2001-2014 Adam Hupp

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.
    ''', module=__name__, name='python-magic', version_string='==0.4.24'
)
