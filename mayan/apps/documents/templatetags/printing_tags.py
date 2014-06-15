from django.template import Library, Node, Variable

from converter.api import get_dimensions

from documents.conf.settings import PRINT_SIZE

register = Library()


class GetImageSizeNode(Node):
    def __init__(self, document):
        self.document = document

    def render(self, context):
        document = Variable(self.document).resolve(context)
        width, height = get_dimensions(document)
        context[u'document_width'], context['document_height'] = width, height
        context[u'document_aspect'] = float(width) / float(height)
        return u''


@register.tag
def get_document_size(parser, token):
    tag_name, arg = token.contents.split(None, 1)

    return GetImageSizeNode(document=arg)
