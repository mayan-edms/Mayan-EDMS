from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db.models.query import QuerySet
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import ungettext, ugettext_lazy as _
from django.views.generic.detail import SingleObjectMixin

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.settings import setting_home_view
from mayan.apps.permissions import Permission

from .compat import FileResponse
from .exceptions import ActionError
from .forms import DynamicForm
from .literals import (
    PK_LIST_SEPARATOR, TEXT_CHOICE_ITEMS, TEXT_CHOICE_LIST,
    TEXT_LIST_AS_ITEMS_PARAMETER, TEXT_LIST_AS_ITEMS_VARIABLE_NAME,
    TEXT_SORT_FIELD_PARAMETER, TEXT_SORT_FIELD_VARIABLE_NAME,
)


class ContentTypeViewMixin:
    """
    This mixin makes it easier for views to retrieve a content type from
    the URL pattern.
    """
    content_type_url_kw_args = {
        'app_label': 'app_label',
        'model_name': 'model_name'
    }

    def get_content_type(self):
        return get_object_or_404(
            klass=ContentType,
            app_label=self.kwargs[
                self.content_type_url_kw_args['app_label']
            ],
            model=self.kwargs[
                self.content_type_url_kw_args['model_name']
            ]
        )


class ExtraDataDeleteViewMixin:
    """
    Mixin to populate the extra data needed for delete views
    """
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if hasattr(self, 'get_instance_extra_data'):
            for key, value in self.get_instance_extra_data().items():
                setattr(self.object, key, value)

        success_url = self.get_success_url()
        if hasattr(self, 'get_delete_extra_data'):
            self.object.delete(**self.get_delete_extra_data())
        else:
            self.object.delete()

        return HttpResponseRedirect(redirect_to=success_url)


class DownloadViewMixin:
    as_attachment = True

    def get_as_attachment(self):
        return self.as_attachment

    def get_download_file_object(self):
        raise NotImplementedError(
            'Class must provide a .get_download_file_object() method that '
            'return a file like object.'
        )

    def get_download_filename(self):
        return None

    def render_to_response(self, **response_kwargs):
        return FileResponse(
            as_attachment=self.get_as_attachment(),
            filename=self.get_download_filename(),
            streaming_content=self.get_download_file_object()
        )


class DynamicFormViewMixin:
    form_class = DynamicForm

    def get_form_kwargs(self):
        data = super().get_form_kwargs()
        data.update({'schema': self.get_form_schema()})
        return data


class ExternalObjectBaseMixin:
    """
    Mixin to allow views to load an object with minimal code but with all
    the filtering and configurability possible. This object is often use as
    the main or master object in multi object views.
    """
    external_object_class = None
    external_object_permission = None
    external_object_pk_url_kwarg = 'pk'
    external_object_pk_url_kwargs = None  # Usage: {'pk': 'pk'}
    external_object_queryset = None

    def get_pk_url_kwargs(self):
        pk_url_kwargs = {}

        if self.external_object_pk_url_kwargs:
            pk_url_kwargs = self.external_object_pk_url_kwargs
        else:
            pk_url_kwargs['pk'] = self.external_object_pk_url_kwarg

        result = {}
        for key, value in pk_url_kwargs.items():
            result[key] = self.kwargs[value]

        return result

    def get_external_object(self):
        return get_object_or_404(
            klass=self.get_external_object_queryset_filtered(),
            **self.get_pk_url_kwargs()
        )

    def get_external_object_permission(self):
        return self.external_object_permission

    def get_external_object_queryset(self):
        if self.external_object_queryset is not None:
            queryset = self.external_object_queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.external_object_class is not None:
            manager = ModelPermission.get_manager(
                model=self.external_object_class
            )
            queryset = manager.all()
        else:
            raise ImproperlyConfigured(
                'View `{}` must provide either an external_object_queryset, '
                'an external_object_class or a custom '
                'get_external_object_queryset() method.'.format(
                    self.__class__.__name__
                )
            )

        return queryset

    def get_external_object_queryset_filtered(self):
        queryset = self.get_external_object_queryset()
        permission = self.get_external_object_permission()

        if permission:
            queryset = AccessControlList.objects.restrict_queryset(
                permission=permission, queryset=queryset,
                user=self.request.user
            )

        return queryset


class ExternalObjectViewMixin(ExternalObjectBaseMixin):
    def dispatch(self, *args, **kwargs):
        self.external_object = self.get_external_object()
        return super().dispatch(*args, **kwargs)


class ExternalContentTypeObjectViewMixin(
    ContentTypeViewMixin, ExternalObjectViewMixin
):
    """
    Mixin to retrieve an external object by content type from the URL pattern.
    """
    external_object_pk_url_kwarg = 'object_id'

    def get_external_object_queryset(self):
        content_type = self.get_content_type()
        self.external_object_class = content_type.model_class()
        return super().get_external_object_queryset()


class ExtraContextViewMixin:
    """
    Mixin that allows views to pass extra context to the template much easier
    than overloading .get_context_data().
    """
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_extra_context())
        return context

    def get_extra_context(self):
        return self.extra_context


class FormExtraKwargsViewMixin:
    """
    Mixin that allows a view to pass extra keyword arguments to forms
    """
    form_extra_kwargs = {}

    def get_form_extra_kwargs(self):
        return self.form_extra_kwargs

    def get_form_kwargs(self):
        result = super().get_form_kwargs()
        result.update(self.get_form_extra_kwargs())
        return result


class ListModeViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if context.get(TEXT_LIST_AS_ITEMS_VARIABLE_NAME):
            default_mode = TEXT_CHOICE_ITEMS
        else:
            default_mode = TEXT_CHOICE_LIST

        list_mode = self.request.GET.get(
            TEXT_LIST_AS_ITEMS_PARAMETER, default_mode
        )

        context.update(
            {
                TEXT_LIST_AS_ITEMS_VARIABLE_NAME: list_mode == TEXT_CHOICE_ITEMS
            }
        )
        return context


class MultipleObjectViewMixin(SingleObjectMixin):
    """
    Mixin that allows a view to work on a single or multiple objects. It can
    receive a pk, a slug or a list of IDs via an id_list query.
    The pk, slug, and ID list parameter name can be changed using the
    attributes: pk_url_kwargs, slug_url_kwarg, and pk_list_key.
    """
    pk_list_key = 'id_list'
    pk_list_separator = PK_LIST_SEPARATOR

    def dispatch(self, request, *args, **kwargs):
        self.object_list = self.get_object_list()
        if self.view_mode_single:
            self.object = self.object_list.first()

        return super().dispatch(request=request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Override BaseDetailView.get()
        """
        return super(SingleObjectMixin, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Override SingleObjectMixin.get_context_data()
        """
        return super(SingleObjectMixin, self).get_context_data(**kwargs)

    def get_object(self):
        """
        Remove this method from the subclass
        """
        raise AttributeError

    def get_object_list(self, queryset=None):
        """
        Returns the list of objects the view is displaying.

        By default this requires `self.queryset` and a `pk`, `slug` ro
        `pk_list' argument in the URLconf, but subclasses can override this
        to return any object.
        """
        self.view_mode_single = False
        self.view_mode_multiple = False

        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        pk_list = self.get_pk_list()

        if pk is not None:
            queryset = queryset.filter(pk=pk)
            self.view_mode_single = True

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})
            self.view_mode_single = True

        if pk_list is not None:
            queryset = queryset.filter(pk__in=pk_list)
            self.view_mode_multiple = True

        # If none of those are defined, it's an error.
        if pk is None and slug is None and pk_list is None:
            raise AttributeError(
                'View %s must be called with '
                'either an object pk, a slug or an pk list.'
                % self.__class__.__name__
            )

        try:
            # Get the single item from the filtered queryset
            queryset.get()
        except queryset.model.MultipleObjectsReturned:
            # Queryset has more than one item, this is good.
            return queryset
        except queryset.model.DoesNotExist:
            raise Http404(
                _('No %(verbose_name)s found matching the query') %
                {'verbose_name': queryset.model._meta.verbose_name}
            )
        else:
            # Queryset has one item, this is good.
            return queryset

    def get_pk_list(self):
        # Accept pk_list even on POST request to allowing direct requests
        # to the view bypassing the initial GET request to submit the form.
        # Example: when the view is called from a test or a custom UI
        result = self.request.GET.get(
            self.pk_list_key, self.request.POST.get(self.pk_list_key)
        )

        if result:
            return result.split(self.pk_list_separator)
        else:
            return None


class ObjectActionViewMixin:
    """
    Mixin that performs a user action to a queryset
    """
    error_message = _('Unable to perform operation on object %(instance)s; %(exception)s.')
    post_object_action_url = None
    success_message_single = _('Operation performed on %(object)s.')
    success_message_singular = _('Operation performed on %(count)d object.')
    success_message_plural = _('Operation performed on %(count)d objects.')
    title_single = _('Perform operation on %(object)s.')
    title_singular = _('Perform operation on %(count)d object.')
    title_plural = _('Perform operation on %(count)d objects.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = None

        if self.view_mode_single:
            title = self.title_single % {'object': self.object}
        elif self.view_mode_multiple:
            title = ungettext(
                singular=self.title_singular,
                plural=self.title_plural,
                number=self.object_list.count()
            ) % {
                'count': self.object_list.count(),
            }

        context['title'] = title

        return context

    def get_post_object_action_url(self):
        return self.post_object_action_url

    def get_success_message(self, count):
        if self.view_mode_single:
            return self.success_message_single % {'object': self.object}

        if self.view_mode_multiple:
            return ungettext(
                singular=self.success_message_singular,
                plural=self.success_message_plural,
                number=count
            ) % {
                'count': count,
            }

    def object_action(self, instance, form=None):
        # User supplied method
        raise NotImplementedError

    def view_action(self, form=None):
        self.action_count = 0
        self.action_id_list = []

        for instance in self.object_list:
            try:
                self.object_action(form=form, instance=instance)
            except ActionError as exception:
                messages.error(
                    message=self.error_message % {
                        'exception': exception, 'instance': instance
                    }, request=self.request
                )
            else:
                self.action_count += 1
                self.action_id_list.append(instance.pk)

        messages.success(
            message=self.get_success_message(count=self.action_count),
            request=self.request
        )

        # Allow get_post_object_action_url to override the redirect URL with a
        # calculated URL after all objects are processed.
        success_url = self.get_post_object_action_url()
        if success_url:
            self.success_url = success_url


class ObjectNameViewMixin:
    def get_object_name(self, context=None):
        if not context:
            context = self.get_context_data()

        object_name = context.get('object_name')

        if not object_name:
            view_object = getattr(self, 'object', context['object'])
            try:
                object_name = view_object._meta.verbose_name
            except AttributeError:
                object_name = _('Object')

        return object_name


class RedirectionViewMixin:
    action_cancel_redirect = None
    next_url = None
    previous_url = None
    post_action_redirect = None
    success_url = None

    def get_action_cancel_redirect(self):
        return self.action_cancel_redirect

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'next': self.get_next_url(),
                'previous': self.get_previous_url()
            }
        )

        return context

    def get_post_action_redirect(self):
        return self.post_action_redirect

    def get_next_url(self):
        if self.next_url:
            return self.next_url
        else:
            post_action_redirect = self.get_post_action_redirect()

            return self.request.POST.get(
                'next', self.request.GET.get(
                    'next', post_action_redirect if post_action_redirect else self.request.META.get(
                        'HTTP_REFERER', reverse(setting_home_view.value)
                    )
                )
            )

    def get_previous_url(self):
        if self.previous_url:
            return self.previous_url
        else:
            action_cancel_redirect = self.get_action_cancel_redirect()

            return self.request.POST.get(
                'previous', self.request.GET.get(
                    'previous', action_cancel_redirect if action_cancel_redirect else self.request.META.get(
                        'HTTP_REFERER', reverse(setting_home_view.value)
                    )
                )
            )

    def get_success_url(self):
        return self.success_url or self.get_next_url() or self.get_previous_url()


class RestrictedQuerysetViewMixin:
    """
    Restrict the view's queryset against a permission via ACL checking.
    Used to restrict the object list of a multiple object view or the source
    queryset of the .get_object() method.
    """
    model = None
    object_permission = None
    source_queryset = None

    def get_object_permission(self):
        return self.object_permission

    def get_queryset(self):
        queryset = self.get_source_queryset()
        object_permission = self.get_object_permission()

        if object_permission:
            queryset = AccessControlList.objects.restrict_queryset(
                permission=object_permission, queryset=queryset,
                user=self.request.user
            )

        return queryset

    def get_source_queryset(self):
        if self.source_queryset is None:
            if self.model:
                return self.model._default_manager.all()
            else:
                raise ImproperlyConfigured(
                    '%(cls)s is missing a QuerySet. Define '
                    '%(cls)s.model, %(cls)s.source_queryset, or override '
                    '%(cls)s.get_source_queryset().' % {
                        'cls': self.__class__.__name__
                    }
                )

        return self.source_queryset.all()


class SortingViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                TEXT_SORT_FIELD_VARIABLE_NAME: self.get_sort_fields(),
            }
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        sort_fields = self.get_sort_fields()
        if sort_fields:
            queryset = queryset.order_by(*sort_fields.split(','))

        return queryset

    def get_sort_fields(self):
        return self.request.GET.get(TEXT_SORT_FIELD_PARAMETER)


class ViewPermissionCheckViewMixin:
    """
    Restrict access to the view based on the user's direct permissions from
    roles. This mixing is used for views whose objects don't support ACLs or
    for views that perform actions that are not related to a specify object or
    object's permission like maintenance views.
    """
    view_permission = None

    def dispatch(self, request, *args, **kwargs):
        view_permission = self.get_view_permission()
        if view_permission:
            Permission.check_user_permissions(
                permissions=(view_permission,),
                user=self.request.user
            )

        return super().dispatch(request, *args, **kwargs)

    def get_view_permission(self):
        return self.view_permission
