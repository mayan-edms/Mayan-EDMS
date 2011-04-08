from django.core.exceptions import PermissionDenied
from django.template import TemplateSyntaxError, Library, \
                            Node, Variable

from permissions.api import check_permissions as check_permission_function

register = Library()


class CheckPermissionsNode(Node):
    def __init__(self, requester, namespace, permission_list, *args, **kwargs):
        self.requester = requester
        self.namespace = namespace
        self.permission_list = permission_list

    def render(self, context):
        requester = Variable(self.requester).resolve(context)
        namespace = Variable(self.namespace).resolve(context)
        permission_list = Variable(self.permission_list).resolve(context)
        try:
            check_permission_function(requester, namespace, permission_list)
            context['permission'] = True
            return ''
        except PermissionDenied:
            context['permission'] = False
            return ''


@register.tag
def check_permissions(parser, token):
    try:
        # Splitting by None == splitting by spaces.
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise TemplateSyntaxError('%r tag requires arguments' % token.contents.split()[0])

    return CheckPermissionsNode(*args.split())
