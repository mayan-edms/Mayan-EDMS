from __future__ import unicode_literals

from django.template import Library, Node, Variable

from converter.api import get_dimensions

register = Library()


class GetImageSizeNode(Node):
    def __init__(self, document):
        self.document = document

    def render(self, context):
        document = Variable(self.document).resolve(context)
        width, height = get_dimensions(document)
        context['document_width'], context['document_height'] = width, height
        context['document_aspect'] = float(width) / float(height)
        return ''


@register.tag
def get_document_size(parser, token):
    tag_name, arg = token.contents.split(None, 1)

    return GetImageSizeNode(document=arg)
