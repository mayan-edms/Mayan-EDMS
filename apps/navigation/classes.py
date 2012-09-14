from __future__ import absolute_import

import urlparse
import urllib
import logging
import re

from django.utils.translation import ugettext_lazy as _
from django.template import VariableDoesNotExist, Variable
from django.utils.encoding import smart_str, smart_unicode
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.http import urlquote, urlencode

from .utils import resolve_to_name, resolve_arguments

logger = logging.getLogger(__name__)


class ResolvedLink(object):
    active = False
    url = '#'
    text = _('Unnamed link')


class Link(object):
    def __init__(self, text, view, klass=None, args=None, sprite=None,
        icon=None, permissions=None, condition=None, conditional_disable=None,
        description=None, dont_mark_active=False, children_view_regex=None,
        keep_query=False, children_classes=None, children_url_regex=None,
        children_views=None, conditional_highlight=None):

        self.text = text
        self.view = view
        self.args = args or {}
        #self.kwargs = kwargs or {}
        self.sprite = sprite
        self.icon = icon
        self.permissions = permissions or []
        self.condition = condition
        self.conditional_disable = conditional_disable
        self.description = description
        self.dont_mark_active = dont_mark_active
        self.klass = klass
        self.keep_query = keep_query
        self.conditional_highlight = conditional_highlight  # Used by dynamic sources
        self.children_views = children_views or []
        self.children_classes = children_classes or []
        self.children_url_regex = children_url_regex or []
        self.children_view_regex = children_view_regex or []

    def resolve(self, context, request=None, current_path=None, current_view=None):
        # Don't calculate these if passed in an argument
        request = request or Variable('request').resolve(context)
        current_path = current_path or request.META['PATH_INFO']
        current_view = current_view or resolve_to_name(current_path)

        # Preserve unicode data in URL query
        previous_path = smart_unicode(urllib.unquote_plus(smart_str(request.get_full_path()) or smart_str(request.META.get('HTTP_REFERER', u'/'))))
        query_string = urlparse.urlparse(previous_path).query
        parsed_query_string = urlparse.parse_qs(query_string)

        logger.debug('condition: %s', self.condition)

        # Check to see if link has conditional display
        if self.condition:
            self.condition_result = self.condition(context)
        else:
            self.condition_result = True

        logger.debug('self.condition_result: %s', self.condition_result)

        if self.condition_result:
            resolved_link = ResolvedLink()
            resolved_link.text = self.text
            resolved_link.sprite = self.sprite
            resolved_link.icon = self.icon
            resolved_link.permissions = self.permissions
            resolved_link.condition_result = self.condition_result

            try:
                #args, kwargs = resolve_arguments(context, self.get('args', {}))
                args, kwargs = resolve_arguments(context, self.args)
            except VariableDoesNotExist:
                args = []
                kwargs = {}

            if self.view:
                if not self.dont_mark_active:
                    resolved_link.active = self.view == current_view

                try:
                    if kwargs:
                        resolved_link.url = reverse(self.view, kwargs=kwargs)
                    else:
                        resolved_link.url = reverse(self.view, args=args)
                        if self.keep_query:
                            resolved_link.url = u'%s?%s' % (urlquote(resolved_link.url), urlencode(parsed_query_string, doseq=True))

                except NoReverseMatch, exc:
                    resolved_link.url = '#'
                    resolved_link.error = exc
            elif self.url:
                if not self.dont_mark_active:
                    resolved_link.url.active = self.url == current_path

                if kwargs:
                    resolved_link.url = self.url % kwargs
                else:
                    resolved_link.url = self.url % args
                    if self.keep_query:
                        resolved_link.url = u'%s?%s' % (urlquote(resolved_link.url), urlencode(parsed_query_string, doseq=True))
            else:
                resolved_link.active = False

            if self.conditional_highlight:
                resolved_link.active = self.conditional_highlight(context)

            if self.conditional_disable:
                resolved_link.disabled = self.conditional_disable(context)
            else:
                resolved_link.disabled = False

            if current_view in self.children_views:
                resolved_link.active = True

            # TODO: eliminate url_regexes and use new tree base main menu
            for child_url_regex in self.children_url_regex:
                if re.compile(child_url_regex).match(current_path.lstrip('/')):
                    resolved_link.active = True

            for children_view_regex in self.children_view_regex:
                if re.compile(children_view_regex).match(current_view):
                    resolved_link.active = True

            for cls in self.children_classes:
                object_list = get_navigation_objects(context)
                if object_list:
                    if type(object_list[0]['object']) == cls or object_list[0]['object'] == cls:
                        #new_link['active'] = True
                        resolved_link.active = True

            return resolved_link
