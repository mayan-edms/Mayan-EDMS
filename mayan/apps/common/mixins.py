from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse

from acls.models import AccessEntry
from permissions.models import Permission


class ExtraContextMixin(object):
    extra_context = {}

    def get_extra_context(self):
        return self.extra_context

    def get_context_data(self, **kwargs):
        context = super(ExtraContextMixin, self).get_context_data(**kwargs)
        context.update(self.get_extra_context())
        return context


class ObjectListPermissionFilterMixin(object):
    object_permission = None

    def get_queryset(self):
        queryset = super(ObjectListPermissionFilterMixin, self).get_queryset()

        if self.object_permission:
            try:
                # Check to see if the user has the permissions globally
                Permission.objects.check_permissions(self.request.user, [self.object_permission])
            except PermissionDenied:
                # No global permission, filter ther queryset per object + permission
                return AccessEntry.objects.filter_objects_by_access(self.object_permission, self.request.user, queryset)
            else:
                # Has the permission globally, return all results
                return queryset
        else:
            return queryset


class ObjectPermissionCheckMixin(object):
    object_permission = None

    def dispatch(self, request, *args, **kwargs):

        if self.object_permission:
            try:
                Permission.objects.check_permissions(request.user, [self.object_permission])
            except PermissionDenied:
                AccessEntry.objects.check_access(self.object_permission, request.user, self.get_object())

        return super(ObjectPermissionCheckMixin, self).dispatch(request, *args, **kwargs)


class RedirectionMixin(object):
    post_action_redirect = None

    def dispatch(self, request, *args, **kwargs):
        self.next_url = self.request.POST.get('next', self.request.GET.get('next', self.post_action_redirect if self.post_action_redirect else self.request.META.get('HTTP_REFERER', reverse('main:home'))))
        self.previous_url = self.request.POST.get('previous', self.request.GET.get('previous', self.request.META.get('HTTP_REFERER', reverse('main:home'))))

        return super(RedirectionMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RedirectionMixin, self).get_context_data(**kwargs)
        context.update(
            {
                'next': self.next_url,
                'previous': self.previous_url
            }
        )

        return context


class ViewPermissionCheckMixin(object):
    view_permission = None

    def dispatch(self, request, *args, **kwargs):
        if self.view_permission:
            Permission.objects.check_permissions(self.request.user, [self.view_permission])

        return super(ViewPermissionCheckMixin, self).dispatch(request, *args, **kwargs)
