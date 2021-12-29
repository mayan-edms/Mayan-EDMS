import logging

from furl import furl

from django.apps import apps
from django.contrib.admin.utils import (
    help_text_for_field, label_for_field
)
from django.core.exceptions import (
    FieldDoesNotExist, ImproperlyConfigured, PermissionDenied
)
from django.db.models.constants import LOOKUP_SEP
from django.template import RequestContext, Variable, VariableDoesNotExist
from django.template.defaulttags import URLNode
from django.urls import resolve, reverse
from django.utils.encoding import force_str, force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.settings import setting_home_view
from mayan.apps.common.utils import get_related_field, resolve_attribute
from mayan.apps.permissions import Permission
from mayan.apps.views.icons import icon_sort_down, icon_sort_up
from mayan.apps.views.literals import (
    TEXT_SORT_FIELD_PARAMETER, TEXT_SORT_FIELD_VARIABLE_NAME
)

from .html_widgets import SourceColumnLinkWidget
from .utils import get_current_view_name

logger = logging.getLogger(name=__name__)


class TemplateObjectMixin:
    def check_condition(self, context, resolved_object=None):
        """
        Check to see if menu has a conditional display function and return
        the result of the condition function against the context.
        """
        if self.condition:
            return self.condition(
                context=context, resolved_object=resolved_object
            )
        else:
            return True

    def get_request(self, context, request=None):
        if not request:
            # Try to get the request object the faster way and fallback to
            # the slower method.
            try:
                request = context.request
            except AttributeError:
                # Simple request extraction failed. Might not be a view
                # context. Try alternate method.
                try:
                    request = Variable(var='request').resolve(context=context)
                except VariableDoesNotExist:
                    # There is no request variable, most probable a 500 in
                    # a test view. Don't return any resolved links then.
                    logger.warning(
                        'No request variable, aborting `{}` resolution'.format(self.__class__.__name__)
                    )
                    raise

        return request


class Link(TemplateObjectMixin):
    _registry = {}

    @staticmethod
    def conditional_active_by_view_name(context, resolved_link):
        return resolved_link.link.view == resolved_link.current_view_name

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def remove(cls, name):
        del cls._registry[name]

    def __init__(
        self, text=None, view=None, args=None, badge_text=None, condition=None,
        conditional_active=None, conditional_disable=None, description=None,
        html_data=None, html_extra_classes=None, icon=None,
        keep_query=False, kwargs=None, name=None, permissions=None,
        query=None, remove_from_query=None, tags=None, url=None
    ):
        self.args = args or []
        self.badge_text = badge_text
        self.condition = condition
        self.conditional_active = conditional_active or Link.conditional_active_by_view_name
        self.conditional_disable = conditional_disable
        self.description = description
        self.html_data = html_data
        self.html_extra_classes = html_extra_classes
        self.icon = icon
        self.keep_query = keep_query
        self.kwargs = kwargs or {}
        self.name = name
        self.permissions = permissions or []
        self.query = query or {}
        self.remove_from_query = remove_from_query or []
        self.tags = tags
        self.text = text
        self.view = view
        self.url = url

        if name:
            self.__class__._registry[name] = self

    def resolve(self, context=None, request=None, resolved_object=None):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )

        if not context and not request:
            raise ImproperlyConfigured(
                'Must provide a context or a request in order to resolve the '
                'link.'
            )

        if not context:
            context = RequestContext(request=request)

        request = self.get_request(context=context, request=request)

        current_path = request.META['PATH_INFO']
        current_view_name = resolve(path=current_path).view_name

        # ACL is tested against the resolved_object or just {{ object }}
        # if not.
        if not resolved_object:
            try:
                resolved_object = Variable(var='object').resolve(context=context)
            except VariableDoesNotExist:
                """No object variable in the context"""

        # If this link has a required permission check that the user has it
        # too.
        if self.permissions:
            if resolved_object:
                try:
                    AccessControlList.objects.check_access(
                        obj=resolved_object, permissions=self.permissions,
                        user=request.user
                    )
                except PermissionDenied:
                    return None
            else:
                try:
                    Permission.check_user_permissions(
                        permissions=self.permissions, user=request.user
                    )
                except PermissionDenied:
                    return None

        # If we were passed an instance of the view context object we are
        # resolving, inject it into the context. This help resolve links for
        # object lists.
        if resolved_object:
            context['resolved_object'] = resolved_object

        # Check to see if link has conditional display function and only
        # display it if the result of the conditional display function is
        # True.
        if not self.check_condition(context=context, resolved_object=resolved_object):
            return None

        resolved_link = ResolvedLink(
            current_view_name=current_view_name, link=self
        )

        if self.view:
            view_name = Variable(var='"{}"'.format(self.view))
            if isinstance(self.args, list) or isinstance(self.args, tuple):
                args = [Variable(var=arg) for arg in self.args]
            else:
                args = [Variable(var=self.args)]

            try:
                kwargs = self.kwargs(context)
            except TypeError:
                # Is not a callable.
                kwargs = self.kwargs

            kwargs = {key: Variable(var=value) for key, value in kwargs.items()}

            # Use Django's exact {% url %} code to resolve the link.
            node = URLNode(
                view_name=view_name, args=args, kwargs=kwargs, asvar=None
            )
            try:
                resolved_link.url = node.render(context=context)
            except VariableDoesNotExist as exception:
                """Not critical, ignore"""
                logger.debug(
                    'VariableDoesNotExist when resolving link "%s" URL; %s',
                    self.text, exception
                )
            except Exception as exception:
                logger.error(
                    'Error resolving link "%s" URL; %s', self.text, exception,
                    exc_info=True
                )
        elif self.url:
            resolved_link.url = self.url

        # This is for links that should be displayed but that are not
        # clickable.
        if self.conditional_disable:
            resolved_link.disabled = self.conditional_disable(context=context)
        else:
            resolved_link.disabled = False

        # Lets a new link keep the same URL query string of the current URL.
        if self.keep_query:
            # Sometimes we are required to remove a key from the URL QS.
            parsed_url = furl(
                force_str(
                    request.get_full_path() or request.META.get(
                        'HTTP_REFERER', reverse(setting_home_view.value)
                    )
                )
            )

            for key in self.remove_from_query:
                try:
                    parsed_url.query.remove(key)
                except KeyError:
                    pass

            # Use the link's URL but with the previous URL querystring.
            new_url = furl(url=resolved_link.url)
            new_url.args = parsed_url.querystr
            resolved_link.url = new_url.url

        if self.query:
            new_url = furl(url=resolved_link.url)
            for key, value in self.query.items():
                try:
                    value = Variable(var=value).resolve(context=context)
                except VariableDoesNotExist:
                    """
                    Not fatal. Variable resolution here is perform as if
                    resolving a template variable. Non existing results
                    are not updated.
                    """
                else:
                    new_url.args[key] = value

            resolved_link.url = new_url.url

        resolved_link.context = context
        return resolved_link


class Menu(TemplateObjectMixin):
    _registry = {}

    @staticmethod
    def get_result_label(item):
        """
        Method to help sort results by label.
        """
        if isinstance(item, ResolvedLink):
            return str(item.link.text)
        else:
            return str(item.label)

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def remove(cls, name):
        del cls._registry[name]

    def __init__(
        self, name, condition=None, icon=None, label=None,
        non_sorted_sources=None
    ):
        if name in self.__class__._registry:
            raise Exception('A menu with this name already exists')

        self.bound_links = {}
        self.condition = condition
        self.excluded_links = {}
        self.icon = icon
        self.label = label
        self.link_positions = {}
        self.name = name
        self.non_sorted_sources = non_sorted_sources or []
        self.proxy_inclusions = set()
        self.unbound_links = {}
        self.__class__._registry[name] = self

    def __repr__(self):
        return '<Menu: {}>'.format(self.name)

    def _map_links_to_source(self, links, source, map_variable, position=None):
        source_links = getattr(self, map_variable).setdefault(source, [])

        position = position or len(source_links)

        for link_index, link in enumerate(iterable=links):
            source_links.append(link)
            self.link_positions[link] = position + link_index

    def add_proxy_inclusions(self, source):
        self.proxy_inclusions.add(source)

    def add_unsorted_source(self, source):
        self.non_sorted_sources.append(source)

    def bind_links(self, links, exclude=None, sources=None, position=None):
        """
        Associate a link to a model, a view inside this menu.
        """
        try:
            for source in sources:
                self._map_links_to_source(
                    links=links, map_variable='bound_links',
                    position=position, source=source
                )
            for source in exclude:
                self._map_links_to_source(
                    links=links, map_variable='excluded_links',
                    position=position, source=source
                )
        except TypeError:
            # Unsourced links display always.
            self._map_links_to_source(
                links=links, map_variable='bound_links',
                position=position, source=sources
            )

    def get_resolved_navigation_object_list(self, context, source):
        resolved_navigation_object_list = []

        if source:
            resolved_navigation_object_list = [source]
        else:
            navigation_object_list = context.get(
                'navigation_object_list', ('object',)
            )

            logger.debug('navigation_object_list: %s', navigation_object_list)

            # Multiple objects
            for navigation_object in navigation_object_list:
                try:
                    resolved_navigation_object_list.append(
                        Variable(var=navigation_object).resolve(context=context)
                    )
                except VariableDoesNotExist:
                    pass

        logger.debug(
            'resolved_navigation_object_list: %s',
            force_text(s=resolved_navigation_object_list)
        )
        return resolved_navigation_object_list

    def get_result_position(self, item):
        """
        Method to help sort results by position.
        """
        if isinstance(item, ResolvedLink):
            return self.link_positions.get(item.link, 0)
        else:
            return self.link_positions.get(item, 0) or 0

    def get_links_for(self, resolved_navigation_object):
        matched_links = set()

        try:
            # Try it as a queryset.
            model = resolved_navigation_object.model
        except AttributeError:
            if isinstance(resolved_navigation_object, str) or resolved_navigation_object is None:
                try:
                    # Try a direct match. Such as strings for view names.
                    matched_links.update(
                        set(
                            self.bound_links[resolved_navigation_object]
                        ) - set(
                            self.unbound_links.get(resolved_navigation_object, ())
                        ) - set(
                            self.excluded_links.get(resolved_navigation_object, ())
                        )
                    )
                except KeyError:
                    return matched_links
            else:
                try:
                    # Try it as a list.
                    item = resolved_navigation_object[0]
                except TypeError:
                    # Neither a queryset nor a list.
                    try:
                        # Try a direct match. Such as strings for view names.
                        matched_links.update(
                            set(
                                self.bound_links[resolved_navigation_object]
                            ) - set(
                                self.unbound_links.get(resolved_navigation_object, ())
                            ) - set(
                                self.excluded_links.get(resolved_navigation_object, ())
                            )
                        )
                    except KeyError:
                        try:
                            # Try as a model instance or model.
                            model = resolved_navigation_object._meta.model
                        except AttributeError:
                            # Not a model instance. Try as subclass
                            # instance, check the class hierarchy.
                            for super_class in resolved_navigation_object.__class__.__mro__[:-1]:
                                matched_links.update(
                                    set(
                                        self.bound_links.get(super_class, ())
                                    ) - set(
                                        self.unbound_links.get(super_class, ())
                                    ) - set(
                                        self.excluded_links.get(resolved_navigation_object, ())
                                    )
                                )
                        else:
                            # Get model link.
                            matched_links.update(
                                set(
                                    self.bound_links.get(model, ())
                                ) - set(
                                    self.unbound_links.get(model, ())
                                ) - set(
                                    self.excluded_links.get(model, ())
                                )
                            )

                            # Get proxy results.
                            # Remove the results explicitly excluded.
                            # Execute after the root model results to allow a proxy
                            # to override an existing results.
                            matched_links.update(
                                set(
                                    self.bound_links.get(model._meta.proxy_for_model, ())
                                ) - set(
                                    self.unbound_links.get(model._meta.proxy_for_model, ())
                                ) - set(
                                    self.excluded_links.get(model, ())
                                )
                            )
                else:
                    # It was is a list.
                    return self.get_links_for(
                        resolved_navigation_object=item
                    )
        else:
            # It was is a queryset.
            return self.get_links_for(
                resolved_navigation_object=model
            )

        return matched_links

    def resolve(self, context=None, request=None, source=None, sort_results=False):
        result = []
        self.matched_link_set = set()

        if not context and not request:
            raise ImproperlyConfigured(
                'Must provide a context or a request in order to resolve '
                'the menu.'
            )

        if not context:
            context = RequestContext(request=request)

        if not self.check_condition(context=context):
            return result

        try:
            request = self.get_request(context=context, request=request)
        except VariableDoesNotExist:
            # Cannot resolve any menus without a request object.
            # Return an empty list.
            return result

        current_view_name = get_current_view_name(request=request)
        if not current_view_name:
            return result

        resolved_navigation_object_list = self.get_resolved_navigation_object_list(
            context=context, source=source
        )

        for resolved_navigation_object in resolved_navigation_object_list:
            matched_links = self.get_links_for(
                resolved_navigation_object=resolved_navigation_object
            )

            result.extend(
                self.resolve_matched_links(
                    context=context,
                    matched_links=matched_links,
                    resolved_navigation_object=resolved_navigation_object,
                    as_resolved_object=True
                )
            )

        # Resolve view links.
        matched_links = self.get_links_for(
            resolved_navigation_object=current_view_name
        )

        result.extend(
            self.resolve_matched_links(
                context=context,
                matched_links=matched_links,
                resolved_navigation_object=current_view_name
            )
        )

        # Resolve "always one" menu links.
        matched_links = self.get_links_for(
            resolved_navigation_object=None
        )

        result.extend(
            self.resolve_matched_links(
                context=context,
                matched_links=matched_links,
                resolved_navigation_object=None
            )
        )

        # Sort links.
        if result:
            unsorted_source = False
            for resolved_navigation_object in resolved_navigation_object_list:
                for source in self.non_sorted_sources:
                    if isinstance(resolved_navigation_object, source):
                        unsorted_source = True
                        break

            if sort_results and not unsorted_source:
                for link_group in result:
                    link_group['links'].sort(key=Menu.get_result_label)
            else:
                for link_group in result:
                    link_group['links'].sort(key=self.get_result_position)

        return result

    def resolve_matched_links(
        self, context, matched_links, resolved_navigation_object,
        as_resolved_object=False
    ):
        result = []

        object_resolved_links = []

        # Deduplicate matched links.
        matched_links = list(
            set(matched_links).difference(self.matched_link_set)
        )
        self.matched_link_set.update(matched_links)

        for link in matched_links:
            kwargs = {
                'context': context
            }

            if as_resolved_object:
                kwargs['resolved_object'] = resolved_navigation_object

            if isinstance(link, Menu):
                condition = link.check_condition(**kwargs)
                if condition:
                    object_resolved_links.append(link)
            else:
                # "Always show" links.
                resolved_link = link.resolve(**kwargs)
                if resolved_link:
                    object_resolved_links.append(resolved_link)

        if object_resolved_links:
            result.append(
                {
                    'object': resolved_navigation_object,
                    'links': object_resolved_links
                }
            )

        return result

    def unbind_links(self, links, sources=None):
        """
        Allow unbinding links from sources, used to allow 3rd party apps to
        change the link binding of core apps.
        """
        try:
            for source in sources:
                self._map_links_to_source(
                    links=links, source=source, map_variable='unbound_links'
                )
        except TypeError:
            # Unsourced links display always.
            self._map_links_to_source(
                links=links, source=sources, map_variable='unbound_links'
            )


class ResolvedLink:
    def __init__(self, link, current_view_name):
        self.context = None
        self.current_view_name = current_view_name
        self.disabled = False
        self.link = link
        self.request = None
        self.url = '#'

    def __repr__(self):
        return '<ResolvedLink: {}>'.format(self.url)

    @property
    def active(self):
        conditional_active = self.link.conditional_active
        if conditional_active:
            return conditional_active(
                context=self.context, resolved_link=self
            )

    @property
    def badge_text(self):
        if self.link.badge_text:
            return self.link.badge_text(context=self.context)

    @property
    def description(self):
        return self.link.description

    @property
    def html_data(self):
        return self.link.html_data

    @property
    def html_extra_classes(self):
        return self.link.html_extra_classes or ''

    @property
    def icon(self):
        return self.link.icon

    @property
    def tags(self):
        return self.link.tags

    @property
    def text(self):
        try:
            return self.link.text(context=self.context)
        except TypeError:
            return self.link.text


class Separator(Link):
    """
    Menu separator. Renders to an <hr> tag.
    """
    def __init__(self, *args, **kwargs):
        self.icon = None
        self.text = None
        self.view = None

    def resolve(self, *args, **kwargs):
        result = ResolvedLink(current_view_name=None, link=self)
        result.separator = True
        return result


class SourceColumn(TemplateObjectMixin):
    _registry = {}

    @staticmethod
    def get_attribute_recursive(attribute, model):
        """
        Walk over the double underscore (__) separated path to the last
        field. Returns the field name and the corresponding model class.
        Used to introspect the label or short_description of a model's
        attribute.
        """
        last_model = model
        for part in attribute.split(LOOKUP_SEP):
            last_model = model
            try:
                field = model._meta.get_field(part)
            except FieldDoesNotExist:
                break
            else:
                model = field.related_model or field.model

        return part, last_model

    @staticmethod
    def sort(columns):
        columns.sort(key=lambda x: x.order)
        return columns

    @classmethod
    def get_column_matches(cls, source):
        columns = []

        try:
            # Try it as a queryset.
            model = source.model
        except AttributeError:
            try:
                # Try it as a list.
                item = source[0]
            except TypeError:
                # Neither a queryset nor a list.
                try:
                    # Try as a model instance or model.
                    model = source._meta.model
                except AttributeError:
                    # Not a model instance.

                    # Try as subclass instance, check the class hierarchy.
                    for super_class in source.__class__.__mro__[:-1]:
                        columns.extend(cls._registry.get(super_class, ()))

                    return columns
                else:
                    # Get model columns.
                    columns.extend(
                        cls._registry.get(model, ())
                    )

                    # Get proxy columns.
                    # Remove the columns explicitly excluded.
                    # Execute after the root model columns to allow a proxy
                    # to override an existing column.
                    for proxy_column in cls._registry.get(model._meta.proxy_for_model, ()):
                        if model not in proxy_column.excludes:
                            columns.append(proxy_column)

                    return columns
            else:
                # It was is a list.
                return cls.get_column_matches(source=item)
        else:
            # It was is a queryset.
            return cls.get_column_matches(source=model)

    @classmethod
    def get_for_source(
        cls, source, exclude_identifier=False, names=None,
        only_identifier=False
    ):
        # Process columns as a set to avoid duplicate resolved column
        # detection code.
        columns = cls.get_column_matches(source=source)

        if exclude_identifier:
            columns = [column for column in columns if not column.is_identifier]
        else:
            # exclude_identifier and only_identifier and mutually exclusive.
            if only_identifier:
                for column in columns:
                    if column.is_identifier:
                        return (column,)

                # There is no column with the identifier marker.
                return ()

        if names is not None:
            indexed_columns = {
                column.name: column for column in columns
            }

            return [indexed_columns[name] for name in names]

        columns = SourceColumn.sort(columns=columns)

        return columns

    def __init__(
        self, source, attribute=None, empty_value=None, func=None,
        help_text=None, html_extra_classes=None, include_label=False,
        is_attribute_absolute_url=False, is_object_absolute_url=False,
        is_identifier=False, is_sortable=False, kwargs=None, label=None,
        name=None, order=None, sort_field=None, widget=None
    ):
        """
        name: optional unique identifier for this source column for the
        specified source.
        """
        self._label = label
        self._help_text = help_text
        self.source = source
        self.attribute = attribute
        self.empty_value = empty_value
        self.excludes = set()
        self.func = func
        self.html_extra_classes = html_extra_classes or ''
        self.include_label = include_label
        self.is_attribute_absolute_url = is_attribute_absolute_url
        self.is_object_absolute_url = is_object_absolute_url
        self.is_identifier = is_identifier
        self.is_sortable = is_sortable
        self.kwargs = kwargs or {}
        self.name = name
        self.order = order or 0
        self.sort_field = sort_field
        self.widget = widget

        if self.is_attribute_absolute_url or self.is_object_absolute_url:
            if not self.widget:
                self.widget = SourceColumnLinkWidget

        self.__class__._registry.setdefault(source, [])
        self.__class__._registry[source].append(self)

        self._calculate_label()
        self._calculate_help_text()
        if self.is_sortable:
            field_name = self.sort_field or self.attribute
            try:
                get_related_field(
                    model=self.source, related_field_name=field_name
                )
            except FieldDoesNotExist as exception:
                raise ImproperlyConfigured(
                    '"{}" is not a field of "{}", cannot be used as a '
                    'sortable column.'.format(field_name, self.source)
                ) from exception

    def _calculate_help_text(self):
        if not self._help_text:
            if self.attribute:
                try:
                    attribute = resolve_attribute(
                        obj=self.source, attribute=self.attribute
                    )
                    self._help_text = getattr(attribute, 'help_text')
                except AttributeError:
                    try:
                        name, model = SourceColumn.get_attribute_recursive(
                            attribute=self.attribute, model=self.source._meta.model
                        )
                        self._help_text = help_text_for_field(
                            name=name, model=model
                        )
                    except AttributeError:
                        self._help_text = None

        self.help_text = self._help_text

    def _calculate_label(self):
        if not self._label:
            if self.attribute:
                try:
                    attribute = resolve_attribute(
                        obj=self.source, attribute=self.attribute
                    )
                    self._label = getattr(attribute, 'short_description')
                except AttributeError:
                    try:
                        name, model = SourceColumn.get_attribute_recursive(
                            attribute=self.attribute, model=self.source._meta.model
                        )
                        self._label = label_for_field(
                            name=name, model=model
                        )
                    except AttributeError:
                        self._label = self.attribute
            else:
                self._label = getattr(
                    self.func, 'short_description', _('Unnamed function')
                )

        self.label = self._label

    def add_exclude(self, source):
        self.excludes.add(source)

    def get_absolute_url(self, obj):
        if self.is_object_absolute_url:
            return obj.get_absolute_url()
        elif self.is_attribute_absolute_url:
            result = resolve_attribute(
                attribute=self.attribute, kwargs=self.kwargs,
                obj=obj
            )
            if result:
                return result.get_absolute_url()

    def get_previous_sort_fields(self, context):
        previous_sort_fields = context.get(TEXT_SORT_FIELD_VARIABLE_NAME, None)

        if previous_sort_fields:
            previous_sort_fields = previous_sort_fields.split(',')
        else:
            previous_sort_fields = ()

        return previous_sort_fields

    def get_sort_field(self):
        if self.sort_field:
            return self.sort_field
        else:
            return self.attribute

    def get_sort_field_querystring(self, context):
        request = self.get_request(context=context)

        # We do this to get an mutable copy we can modify.
        querystring = request.GET.copy()

        previous_sort_fields = self.get_previous_sort_fields(context=context)

        sort_field = self.get_sort_field()

        if sort_field in previous_sort_fields:
            result = '-{}'.format(sort_field)
        else:
            result = '{}'.format(sort_field)

        querystring[TEXT_SORT_FIELD_PARAMETER] = result

        return '?{}'.format(querystring.urlencode())

    def get_sort_icon(self, context):
        previous_sort_fields = self.get_previous_sort_fields(context=context)
        sort_field = self.get_sort_field()

        if sort_field in previous_sort_fields:
            return icon_sort_down
        elif '-{}'.format(sort_field) in previous_sort_fields:
            return icon_sort_up

    def resolve(self, context):
        if self.attribute:
            result = resolve_attribute(
                attribute=self.attribute, kwargs=self.kwargs,
                obj=context['object']
            )
        elif self.func:
            result = self.func(context=context, **self.kwargs)
        else:
            result = context['object']

        self.absolute_url = self.get_absolute_url(obj=context['object'])
        if self.widget:
            try:
                request = self.get_request(context=context)
            except VariableDoesNotExist:
                """
                Don't attempt to render and return the value if any.
                """
            else:
                widget_instance = self.widget(
                    column=self, request=request
                )
                return widget_instance.render(value=result)

        if not result:
            if self.empty_value:
                return self.empty_value
            else:
                return result
        else:
            return result


class Text(Link):
    """
    Menu text. Renders to a plain <li> tag.
    """
    def __init__(self, *args, **kwargs):
        self.html_extra_classes = kwargs.get('html_extra_classes', '')
        self.icon = None
        self.text = kwargs.get('text')
        self.view = None

    def resolve(self, *args, **kwargs):
        result = ResolvedLink(current_view_name=None, link=self)
        result.context = kwargs.get('context')
        result.text_span = True
        return result
