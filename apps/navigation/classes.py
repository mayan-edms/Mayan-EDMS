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
    link_bindings = {}

    @classmethod
    def get_context_navigation_links(cls, context, menu_name=None, links_dict=link_bindings):
        request = Variable('request').resolve(context)
        current_path = request.META['PATH_INFO']
        current_view = resolve_to_name(current_path)
        context_links = {}
        
        # Don't fudge with the original global dictionary
        # TODO: fix this
        links_dict = links_dict.copy()

        # Dynamic sources
        # TODO: improve name to 'injected...'
        try:
            """
            Check for and inject a temporary navigation dictionary
            """
            temp_navigation_links = Variable('temporary_navigation_links').resolve(context)
            if temp_navigation_links:
                links_dict.update(temp_navigation_links)
        except VariableDoesNotExist:
            pass

        try:
            view_links = links_dict[menu_name][current_view]['links']
            if view_links:
                context_links.setdefault(None, [])

            for link in view_links:
                context_links[None].append(link.resolve(context, request=request, current_path=current_path, current_view=current_view))
        except KeyError:
            pass

        for resolved_object, object_properties in get_navigation_objects(context).items():
            try:
                resolved_object_reference = resolved_object
                object_links = links_dict[menu_name][type(resolved_object_reference)]['links']
                if object_links:
                    context_links.setdefault(resolved_object_reference, [])

                for link in object_links:
                    context_links[resolved_object_reference].append(link.resolve(context, request=request, current_path=current_path, current_view=current_view))
            except KeyError:
                pass

        return context_links

    def __init__(self, text, view, klass=None, args=None, icon=None,
        permissions=None, condition=None, conditional_disable=None,
        description=None, dont_mark_active=False, children_view_regex=None,
        keep_query=False, children_classes=None, children_url_regex=None,
        children_views=None, conditional_highlight=None):

        self.text = text
        self.view = view
        self.args = args or {}
        #self.kwargs = kwargs or {}
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
'''
    def bind(self, sources, menu_name=None, position=0):
        """
        Associate a link to a model, a view, or an url
        """
        self.__class__.link_bindings.setdefault(menu_name, {})
        for source in sources:
            self.__class__.link_bindings[menu_name].setdefault(source, {'links': []})
            try:
                self.__class__.link_bindings[menu_name][source]['links'].extend(links)
            except TypeError:
                # Try to see if links is a single link
                self.__class__.link_bindings[menu_name][source]['links'].append(links)
'''
"""
register_model_list_columns(Document, [
        {'name':_(u'thumbnail'), 'attribute':
            encapsulate(lambda x: document_thumbnail(x, gallery_name='document_list', title=x.filename))
        },
    ])
"""
class ModelListColumn(object):
    _model_list_columns = {}

    @classmethod
    def get_model(cls, model):
        return cls._model_list_columns.get(model)

    def __init__(self, model, name, attribute):
        self.__class__._model_list_columns.setdefault(model, [])
        self.__class__._model_list_columns[model].extend(columns)
