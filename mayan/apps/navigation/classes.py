from __future__ import unicode_literals

import inspect
import logging
import urllib
import urlparse

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import resolve, reverse
from django.template import VariableDoesNotExist, Variable
from django.template.defaulttags import URLNode
from django.utils.encoding import smart_str, smart_unicode
from django.utils.http import urlencode, urlquote
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessEntry
from permissions.models import Permission

logger = logging.getLogger(__name__)


class ResolvedLink(object):
    active = False
    description = None
    icon = None
    text = _('Unnamed link')
    url = '#'


class Menu(object):
    # TODO: Add support for position #{'link': links, 'position': position})

    _registry = {}

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    def __init__(self, name):
        if name in self.__class__._registry:
            raise Exception('A menu with this name already exists')

        self.name = name
        self.bound_links = {}
        self.__class__._registry[name] = self

    def _add_links_to_source(self, links, source, position=None):
        source_links = self.bound_links.setdefault(source, [])

        for link in links:
            source_links.append(link)

    def bind_links(self, links, sources=None, position=None):
        """
        Associate a link to a model, a view inside this menu
        """

        if sources:
            for source in sources:
                self._add_links_to_source(links, source)
        else:
            # Unsourced links display always
            self._add_links_to_source(links, None)

    def resolve(self, context, source=None):
        request = Variable('request').resolve(context)
        current_path = request.META['PATH_INFO']

        # Get sources: view name, view objects
        current_view = resolve(current_path).view_name
        resolved_navigation_object_list = []

        result = []

        if source:
            resolved_navigation_object_list = [source]
        else:
            navigation_object_list = context.get('navigation_object_list', ['object'])

            # Multiple objects
            for navigation_object in navigation_object_list:
                try:
                    resolved_navigation_object_list.append(Variable(navigation_object).resolve(context))
                except VariableDoesNotExist:
                    pass

        for resolved_navigation_object in resolved_navigation_object_list:
            for source, links in self.bound_links.iteritems():
                try:
                    if inspect.isclass(source) and isinstance(resolved_navigation_object, source) or source == CombinedSource(obj=resolved_navigation_object, view=current_view):
                        for link in links:
                            resolved_link = link.resolve(context=context, resolved_object=resolved_navigation_object)
                            if resolved_link:
                                result.append(resolved_link)
                        #break  # No need for further content object match testing

                except TypeError:
                    # When source is a dictionary
                    pass

        # View links
        for link in self.bound_links.get(current_view, []):
            resolved_link = link.resolve(context)
            if resolved_link:
                result.append(resolved_link)

        # Main menu links
        for link in self.bound_links.get(None, []):
            resolved_link = link.resolve(context)
            if resolved_link:
                result.append(resolved_link)

        return result


class Link(object):
    def __init__(self, text, view, args=None, condition=None,
                 conditional_disable=None, description=None, icon=None,
                 keep_query=False, klass=None, kwargs=None, permissions=None,
                 remove_from_query=None):

        self.args = args or []
        self.condition = condition
        self.conditional_disable = conditional_disable
        self.description = description
        self.icon = icon
        self.keep_query = keep_query
        self.klass = klass
        self.kwargs = kwargs or {}
        self.permissions = permissions or []
        self.remove_from_query = remove_from_query or []
        self.text = text
        self.view = view

    def resolve(self, context, resolved_object=None):
        request = Variable('request').resolve(context)
        current_path = request.META['PATH_INFO']
        current_view = resolve(current_path).view_name

        # Preserve unicode data in URL query
        previous_path = smart_unicode(urllib.unquote_plus(smart_str(request.get_full_path()) or smart_str(request.META.get('HTTP_REFERER', reverse('main:home')))))
        query_string = urlparse.urlparse(previous_path).query
        parsed_query_string = urlparse.parse_qs(query_string)

        for key in self.remove_from_query:
            try:
                del parsed_query_string[key]
            except KeyError:
                pass

        if self.permissions:
            try:
                Permission.objects.check_permissions(request.user, self.permissions)
            except PermissionDenied:
                if resolved_object:
                    try:
                        AccessEntry.objects.check_access(self.permissions, request.user, resolved_object)
                    except PermissionDenied:
                        return None
                else:
                    return None

        # Check to see if link has conditional display
        if self.condition:
            if not self.condition(context):
                return None

        resolved_link = ResolvedLink()
        resolved_link.description = self.description
        resolved_link.icon = self.icon
        resolved_link.klass = self.klass
        resolved_link.text = self.text

        view_name = Variable('"{}"'.format(self.view))
        if isinstance(self.args, list):
            args = [Variable(arg) for arg in self.args]
        else:
            args = [Variable(self.args)]

        kwargs = {key: Variable(value) for key, value in self.kwargs.iteritems()}

        node = URLNode(view_name=view_name, args=args, kwargs={}, asvar=None)

        if resolved_object:
            context['resolved_object'] = resolved_object

        resolved_link.url = node.render(context)

        if self.conditional_disable:
            resolved_link.disabled = self.conditional_disable(context)
        else:
            resolved_link.disabled = False

        if self.keep_query:
            resolved_link.url = '%s?%s' % (urlquote(resolved_link.url), urlencode(parsed_query_string, doseq=True))

        resolved_link.active = self.view == current_view

        return resolved_link


class ModelListColumn(object):
    _model_list_columns = {}

    @classmethod
    def get_model(cls, model):
        return cls._model_list_columns.get(model)

    def __init__(self, model, name, attribute):
        self.__class__._model_list_columns.setdefault(model, [])
        self.__class__._model_list_columns[model].extend(columns)


class CombinedSource(object):
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
