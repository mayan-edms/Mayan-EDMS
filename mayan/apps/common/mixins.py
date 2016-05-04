from __future__ import unicode_literals

from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ungettext, ugettext_lazy as _

from permissions import Permission

__all__ = (
    'DeleteExtraDataMixin', 'ExtraContextMixin',
    'ObjectListPermissionFilterMixin', 'ObjectNameMixin',
    'ObjectPermissionCheckMixin', 'RedirectionMixin',
    'ViewPermissionCheckMixin'
)


class DeleteExtraDataMixin(object):
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        if hasattr(self, 'get_delete_extra_data'):
            self.object.delete(**self.get_delete_extra_data())
        else:
            self.object.delete()

        return HttpResponseRedirect(success_url)


class ExtraContextMixin(object):
    extra_context = {}

    def get_extra_context(self):
        return self.extra_context

    def get_context_data(self, **kwargs):
        context = super(ExtraContextMixin, self).get_context_data(**kwargs)
        context.update(self.get_extra_context())
        return context


class MultipleInstanceActionMixin(object):
    model = None
    success_message = 'Operation performed on %(count)d object'
    success_message_plural = 'Operation performed on %(count)d objects'

    def get_pk_list(self):
        return self.request.GET.get(
            'id_list', self.request.POST.get('id_list', '')
        ).split(',')

    def get_queryset(self):
        return self.model.objects.filter(pk__in=self.get_pk_list())

    def get_success_message(self, count):
        return ungettext(
            self.success_message,
            self.success_message_plural,
            count
        ) % {
            'count': count,
        }

    def post(self, request, *args, **kwargs):
        count = 0
        for instance in self.get_queryset():
            try:
                self.object_action(instance=instance)
            except PermissionDenied:
                pass
            else:
                count += 1

        messages.success(
            self.request,
            self.get_success_message(count=count)
        )

        return HttpResponseRedirect(self.get_success_url())


class ObjectListPermissionFilterMixin(object):
    object_permission = None

    def get_queryset(self):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )

        queryset = super(ObjectListPermissionFilterMixin, self).get_queryset()

        if self.object_permission:
            try:
                # Check to see if the user has the permissions globally
                Permission.check_permissions(
                    self.request.user, (self.object_permission,)
                )
            except PermissionDenied:
                # No global permission, filter ther queryset per object +
                # permission
                return AccessControlList.objects.filter_by_access(
                    self.object_permission, self.request.user, queryset
                )
            else:
                # Has the permission globally, return all results
                return queryset
        else:
            return queryset


class ObjectNameMixin(object):
    def get_object_name(self, context=None):
        if not context:
            context = self.get_context_data()

        object_name = context.get('object_name')

        if not object_name:
            try:
                object_name = self.object._meta.verbose_name
            except AttributeError:
                object_name = _('Object')

        return object_name


class ObjectPermissionCheckMixin(object):
    object_permission = None

    def get_permission_object(self):
        return self.get_object()

    def dispatch(self, request, *args, **kwargs):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )

        if self.object_permission:
            try:
                Permission.check_permissions(
                    request.user, (self.object_permission,)
                )
            except PermissionDenied:
                AccessControlList.objects.check_access(
                    self.object_permission, request.user,
                    self.get_permission_object(),
                    related=getattr(self, 'object_permission_related', None)
                )

        return super(
            ObjectPermissionCheckMixin, self
        ).dispatch(request, *args, **kwargs)


class RedirectionMixin(object):
    post_action_redirect = None
    action_cancel_redirect = None

    def get_post_action_redirect(self):
        return self.post_action_redirect

    def get_action_cancel_redirect(self):
        return self.action_cancel_redirect

    def dispatch(self, request, *args, **kwargs):
        post_action_redirect = self.get_post_action_redirect()
        action_cancel_redirect = self.get_action_cancel_redirect()

        self.next_url = self.request.POST.get(
            'next', self.request.GET.get(
                'next', post_action_redirect if post_action_redirect else self.request.META.get(
                    'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
                )
            )
        )
        self.previous_url = self.request.POST.get(
            'previous', self.request.GET.get(
                'previous', action_cancel_redirect if action_cancel_redirect else self.request.META.get(
                    'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
                )
            )
        )

        return super(
            RedirectionMixin, self
        ).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RedirectionMixin, self).get_context_data(**kwargs)
        context.update(
            {
                'next': self.next_url,
                'previous': self.previous_url
            }
        )

        return context

    def get_success_url(self):
        return self.next_url or self.previous_url


class ViewPermissionCheckMixin(object):
    view_permission = None

    def dispatch(self, request, *args, **kwargs):
        if self.view_permission:
            Permission.check_permissions(
                requester=self.request.user,
                permissions=(self.view_permission,)
            )

        return super(
            ViewPermissionCheckMixin, self
        ).dispatch(request, *args, **kwargs)
