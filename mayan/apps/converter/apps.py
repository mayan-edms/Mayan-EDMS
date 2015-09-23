from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from common import MayanAppConfig, menu_object, menu_sidebar
from common.classes import Package

from navigation import SourceColumn

from .links import (
    link_transformation_create, link_transformation_delete,
    link_transformation_edit
)
from .models import Transformation


class ConverterApp(MayanAppConfig):
    name = 'converter'
    verbose_name = _('Converter')

    def ready(self):
        super(ConverterApp, self).ready()

        Package(label='Pillow', license_text='''
The Python Imaging Library (PIL) is

    Copyright (c) 1997-2011 by Secret Labs AB
    Copyright (c) 1995-2011 by Fredrik Lundh

By obtaining, using, and/or copying this software and/or its associated documentation, you agree that you have read, understood, and will comply with the following terms and conditions:

Permission to use, copy, modify, and distribute this software and its associated documentation for any purpose and without fee is hereby granted, provided that the above copyright notice appears in all copies, and that both that copyright notice and this permission notice appear in supporting documentation, and that the name of Secret Labs AB or the author not be used in advertising or publicity pertaining to distribution of the software without specific, written prior permission.

SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
        ''')

        SourceColumn(source=Transformation, label=_('Order'), attribute='order')
        SourceColumn(
            source=Transformation, label=_('Transformation'),
            func=lambda context: unicode(context['object'])
        )
        SourceColumn(
            source=Transformation, label=_('Arguments'), attribute='arguments'
        )

        menu_object.bind_links(
            links=(link_transformation_edit, link_transformation_delete),
            sources=(Transformation,)
        )
        menu_sidebar.bind_links(
            links=(link_transformation_create,), sources=(Transformation,)
        )
        menu_sidebar.bind_links(
            links=(link_transformation_create,),
            sources=(
                'converter:transformation_create',
                'converter:transformation_list'
            )
        )
