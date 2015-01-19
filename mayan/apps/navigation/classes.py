from __future__ import unicode_literals

import inspect
import logging
import urllib
import urlparse

from django.core.urlresolvers import NoReverseMatch, resolve, reverse
from django.template import VariableDoesNotExist, Variable
from django.utils.encoding import smart_str, smart_unicode
from django.utils.http import urlencode, urlquote
from django.utils.text import unescape_string_literal
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class ResolvedLink(object):
    active = False
    url = '#'
    text = _('Unnamed link')


class Link(object):
    bound_links = {}

    @classmethod
    def bind_links(cls, sources, links, menu_name=None, position=0):
        """
        Associate a link to a model, a view, or an url
        """
        cls.bound_links.setdefault(menu_name, {})
        try:
            for source in sources:
                cls.bound_links[menu_name].setdefault(source, {'links': []})
                try:
                    cls.bound_links[menu_name][source]['links'].extend(links)
                except TypeError:
                    # Try to see if links is a single link
                    cls.bound_links[menu_name][source]['links'].append(links)
        except TypeError:
            raise Exception('The bind_links source argument must be a list, even for single element sources.')

    def __init__(self, text, view, klass=None, args=None, icon=None,
                 permissions=None, condition=None, conditional_disable=None,
                 description=None, dont_mark_active=False, keep_query=False,
                 conditional_highlight=None):

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

    def resolve(self, context, request=None, current_path=None, current_view=None, resolved_object=None):
        # Don't calculate these if passed in an argument
        request = request or Variable('request').resolve(context)
        current_path = current_path or request.META['PATH_INFO']
        if not current_view:
            match = resolve(current_path)
            if match.namespace:
                current_view = '{}:{}'.format(match.namespace, match.url_name)
            else:
                current_view = match.url_name

        # Preserve unicode data in URL query
        previous_path = smart_unicode(urllib.unquote_plus(smart_str(request.get_full_path()) or smart_str(request.META.get('HTTP_REFERER', reverse('main:home')))))
        query_string = urlparse.urlparse(previous_path).query
        parsed_query_string = urlparse.parse_qs(query_string)

        logger.debug('condition: %s', self.condition)

        if resolved_object:
            context['resolved_object'] = resolved_object

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
                args, kwargs = Link.resolve_arguments(context, self.args)
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
                            resolved_link.url = '%s?%s' % (urlquote(resolved_link.url), urlencode(parsed_query_string, doseq=True))

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
                        resolved_link.url = '%s?%s' % (urlquote(resolved_link.url), urlencode(parsed_query_string, doseq=True))
            else:
                resolved_link.active = False

            if self.conditional_highlight:
                resolved_link.active = self.conditional_highlight(context)

            if self.conditional_disable:
                resolved_link.disabled = self.conditional_disable(context)
            else:
                resolved_link.disabled = False

            # TODO: add tree base main menu support to auto activate parent links

            return resolved_link

    @classmethod
    def get_context_navigation_links(cls, context, menu_name=None, links_dict=None):
        request = Variable('request').resolve(context)
        current_path = request.META['PATH_INFO']
        match = resolve(current_path)
        if match.namespace:
            current_view = '{}:{}'.format(match.namespace, match.url_name)
        else:
            current_view = match.url_name

        context_links = {}
        if not links_dict:
            links_dict = Link.bound_links

        # Don't fudge with the original global dictionary
        # TODO: fix this
        links_dict = links_dict.copy()

        # Dynamic sources
        # TODO: improve name to 'injected...'
        # TODO: remove, only used by staging files
        try:
            # Check for an inject temporary navigation dictionary
            temp_navigation_links = Variable('extra_navigation_links').resolve(context)
            if temp_navigation_links:
                links_dict.update(temp_navigation_links)
        except VariableDoesNotExist:
            pass

        # Get view only links
        try:
            view_links = links_dict[menu_name][current_view]['links']
        except KeyError:
            pass
        else:
            context_links[None] = []

            for link in view_links:
                context_links[None].append(link.resolve(context, request=request, current_path=current_path, current_view=current_view))

        # Get object links
        for resolved_object in Link.get_navigation_objects(context).keys():
            for source, data in links_dict.get(menu_name, {}).items():
                if inspect.isclass(source) and isinstance(resolved_object, source) or Combined(obj=type(resolved_object), view=current_view) == source:
                    context_links[resolved_object] = []
                    for link in data['links']:
                        context_links[resolved_object].append(link.resolve(context, request=request, current_path=current_path, current_view=current_view, resolved_object=resolved_object))
                    break  # No need for further content object match testing
        return context_links

    @classmethod
    def get_navigation_objects(cls, context):
        objects = {}

        try:
            object_list = Variable('navigation_object_list').resolve(context)
        except VariableDoesNotExist:
            pass
        else:
            logger.debug('found: navigation_object_list')
            for obj in object_list:
                objects.setdefault(obj, {})

        # Legacy
        try:
            indirect_reference_list = Variable('navigation_object_list_ref').resolve(context)
        except VariableDoesNotExist:
            pass
        else:
            logger.debug('found: navigation_object_list_ref')
            for indirect_reference in indirect_reference_list:
                try:
                    resolved_object = Variable(indirect_reference['object']).resolve(context)
                except VariableDoesNotExist:
                    resolved_object = None
                else:
                    objects.setdefault(resolved_object, {})
                    objects[resolved_object]['label'] = indirect_reference.get('object_name')

        try:
            resolved_object = Variable('object').resolve(context)
        except VariableDoesNotExist:
            pass
        else:
            logger.debug('found single object')
            try:
                object_label = Variable('object_name').resolve(context)
            except VariableDoesNotExist:
                object_label = None
            finally:
                objects.setdefault(resolved_object, {})
                objects[resolved_object]['label'] = object_label

        return objects

    @classmethod
    def resolve_template_variable(cls, context, name):
        try:
            return unescape_string_literal(name)
        except ValueError:
            #return Variable(name).resolve(context)
            #TODO: Research if should return always as a str
            return str(Variable(name).resolve(context))
        except TypeError:
            return name

    @classmethod
    def resolve_arguments(cls, context, src_args):
        args = []
        kwargs = {}

        if isinstance(src_args, list):
            for i in src_args:
                try:
                    # Try to execute as a function
                    val = i(context=context)
                except TypeError:
                    val = Link.resolve_template_variable(context, i)
                    if val:
                        args.append(val)
                else:
                    args.append(val)
        elif isinstance(src_args, dict):
            for key, value in src_args.items():
                try:
                    # Try to execute as a function
                    val = i(context=context)
                except TypeError:
                    val = Link.resolve_template_variable(context, value)
                    if val:
                        kwargs[key] = val
                else:
                    kwargs[key] = val
        else:
            val = Link.resolve_template_variable(context, src_args)
            if val:
                args.append(val)

        return args, kwargs


class ModelListColumn(object):
    _model_list_columns = {}

    @classmethod
    def get_model(cls, model):
        return cls._model_list_columns.get(model)

    def __init__(self, model, name, attribute):
        self.__class__._model_list_columns.setdefault(model, [])
        self.__class__._model_list_columns[model].extend(columns)


class Combined(object):
    """
    Class that binds a link to a combination of an object and a view.
    This is used to show links relating to a specific object type but only
    in certain views.
    Used by the PageDocument class to show rotatio and zoom link only on
    certain views
    """
    def __init__(self, obj, view):
        self.obj = obj
        self.view = view

    def __hash__(self):
        return hash((self.obj, self.view))

    def __eq__(self, other):
        return hash(self) == hash(other)
