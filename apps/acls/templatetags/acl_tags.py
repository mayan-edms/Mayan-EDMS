from django.core.exceptions import PermissionDenied
from django.template import (TemplateSyntaxError, Library,
    Node, Variable, VariableDoesNotExist)

from acls.models import AccessEntry

register = Library()


class CheckAccessNode(Node):
    def __init__(self, permission_list=None, requester=None, obj=None, *args, **kwargs):
        self.requester = requester
        self.permission_list = permission_list
        self.obj = obj

    def render(self, context):
        permission_list = Variable(self.permission_list).resolve(context)
        try:
            # Check access_object, useful for document_page views
            obj = Variable('access_object').resolve(context)
        except VariableDoesNotExist:
            try:
                obj = Variable(self.obj).resolve(context)
            except VariableDoesNotExist:
                context[u'access'] = True
                return u''
        
        requester = Variable(self.requester).resolve(context)

        if not permission_list or not obj:
            # There is no permissions list to check against which means
            # this link is available for all
            context[u'access'] = True
            return u''

        try:
            AccessEntry.objects.check_accesses(permission_list, requester, obj)
        except PermissionDenied:
            context[u'access'] = False
            return u''
        else:
            context[u'access'] = True
            return u''


@register.tag
def check_access(parser, token):
    try:
        # Splitting by None == splitting by spaces.
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise TemplateSyntaxError(u'%r tag requires arguments' % token.contents.split()[0])

    return CheckAccessNode(*args.split())
