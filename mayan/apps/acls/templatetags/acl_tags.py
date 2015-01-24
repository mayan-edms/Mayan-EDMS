from __future__ import unicode_literals

import logging

from django.core.exceptions import PermissionDenied
from django.template import (
    Library, Node, TemplateSyntaxError, Variable, VariableDoesNotExist
)

from acls.models import AccessEntry

logger = logging.getLogger(__name__)
register = Library()


class CheckAccessNode(Node):
    def __init__(self, permission_list=None, requester=None, obj=None, *args, **kwargs):
        self.requester = requester
        self.permission_list = permission_list
        self.obj = obj

    def render(self, context):
        permission_list = Variable(self.permission_list).resolve(context)
        logger.debug('permission_list: %s', ','.join([unicode(p) for p in permission_list]))

        try:
            # Check access_object, useful for document_page views
            obj = Variable('access_object').resolve(context)
            logger.debug('access_object: %s', obj)
        except VariableDoesNotExist:
            try:
                obj = Variable(self.obj).resolve(context)
                logger.debug('obj: %s', obj)
            except VariableDoesNotExist:
                context['access'] = False
                logger.debug('no obj, access False')
                return ''

        if not permission_list:
            # There is no permissions list to check against which means
            # this link is available for all
            context['access'] = True
            return ''

        requester = Variable(self.requester).resolve(context)
        logger.debug('requester: %s', requester)

        if obj:
            try:
                AccessEntry.objects.check_accesses(permission_list, requester, obj)
            except PermissionDenied:
                context['access'] = False
                logger.debug('access: False')
                return ''
            else:
                context['access'] = True
                logger.debug('access: True')
                return ''
        else:
            context['access'] = False
            logger.debug('No object, access: False')
            return ''


@register.tag
def check_access(parser, token):
    try:
        # Splitting by None == splitting by spaces.
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise TemplateSyntaxError('%r tag requires arguments' % token.contents.split()[0])

    return CheckAccessNode(*args.split())
