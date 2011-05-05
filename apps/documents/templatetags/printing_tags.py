from django.template import TemplateSyntaxError, Library, \
                            VariableDoesNotExist, Node, Variable
from converter.api import get_document_dimensions, QUALITY_PRINT
from documents.views import calculate_converter_arguments
from documents.conf.settings import PRINT_SIZE

register = Library()


class GetImageSizeNode(Node):
    def __init__(self, document):
        self.document = document

    def render(self, context):
        document = Variable(self.document).resolve(context)
        arguments, warnings = calculate_converter_arguments(document, size=PRINT_SIZE, quality=QUALITY_PRINT)
        width, height = get_document_dimensions(document, **arguments)
        context[u'document_width'], context['document_height'] = width, height
        context[u'document_aspect'] = float(width) / float(height)
        return u''
 
@register.tag
def get_document_size(parser, token):
    tag_name, arg = token.contents.split(None, 1)

    return GetImageSizeNode(document=arg)
