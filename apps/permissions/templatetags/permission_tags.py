from django.core.exceptions import PermissionDenied
from django.template import TemplateSyntaxError, Library, \
                            Node, Variable

from permissions.api import check_permissions as check_permission_function

register = Library()


class CheckPermissionsNode(Node):
    def __init__(self, requester, namespace=None, permission_list=None, *args, **kwargs):
        self.requester = requester
        self.namespace = namespace
        self.permission_list = permission_list

    def render(self, context):
        permission_list = Variable(self.permission_list).resolve(context)
        if not permission_list:
            # There is no permissions list to check against which means
            # this link is available for all
            context[u'permission'] = True
            return u''
        requester = Variable(self.requester).resolve(context)
        namespace = Variable(self.namespace).resolve(context)
        try:
            check_permission_function(requester, namespace, permission_list)
            context[u'permission'] = True
            return u''
        except PermissionDenied:
            context[u'permission'] = False
            return u''


@register.tag
def check_permissions(parser, token):
    try:
        # Splitting by None == splitting by spaces.
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise TemplateSyntaxError(u'%r tag requires arguments' % token.contents.split()[0])

    return CheckPermissionsNode(*args.split())
