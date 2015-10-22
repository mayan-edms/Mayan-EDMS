from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from common.views import (
    AssignRemoveView, SingleObjectCreateView, SingleObjectDeleteView,
    SingleObjectEditView, SingleObjectListView
)
from permissions import Permission

from .forms import PasswordForm, UserForm
from .permissions import (
    permission_group_create, permission_group_delete, permission_group_edit,
    permission_group_view, permission_user_create, permission_user_delete,
    permission_user_edit, permission_user_view
)


class GroupCreateView(SingleObjectCreateView):
    extra_context = {'title': _('Create new group')}
    fields = ('name',)
    model = Group
    post_action_redirect = reverse_lazy('user_management:group_list')
    view_permission = permission_group_create


class GroupEditView(SingleObjectEditView):
    fields = ('name',)
    model = Group
    post_action_redirect = reverse_lazy('user_management:group_list')
    view_permission = permission_group_edit

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Edit group: %s') % self.get_object(),
        }


class GroupListView(SingleObjectListView):
    extra_context = {
        'hide_link': True,
        'title': _('Groups'),
    }
    model = Group
    view_permission = permission_group_view


class GroupDeleteView(SingleObjectDeleteView):
    model = Group
    post_action_redirect = reverse_lazy('user_management:group_list')
    view_permission = permission_group_delete

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Delete the group: %s?') % self.get_object(),
        }


class GroupMembersView(AssignRemoveView):
    decode_content_type = True
    left_list_title = _('Available users')
    right_list_title = _('Members of groups')
    view_permission = permission_group_edit

    def add(self, item):
        self.get_object().user_set.add(item)

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Members of group: %s') % self.get_object()
        }

    def get_object(self):
        return get_object_or_404(Group, pk=self.kwargs['pk'])

    def left_list(self):
        return AssignRemoveView.generate_choices(
            User.objects.exclude(
                groups=self.get_object()
            ).exclude(is_staff=True).exclude(is_superuser=True)
        )

    def right_list(self):
        return AssignRemoveView.generate_choices(
            self.get_object().user_set.all()
        )

    def remove(self, item):
        self.get_object().user_set.remove(item)


class UserEditView(SingleObjectEditView):
    fields = ('username', 'first_name', 'last_name', 'email', 'is_active',)
    post_action_redirect = reverse_lazy('user_management:user_list')
    queryset = get_user_model().objects.filter(
        is_superuser=False, is_staff=False
    )
    view_permission = permission_user_edit

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Edit user: %s') % self.get_object(),
        }


class UserGroupsView(AssignRemoveView):
    decode_content_type = True
    left_list_title = _('Available groups')
    right_list_title = _('Groups joined')
    view_permission = permission_user_edit

    def add(self, item):
        item.user_set.add(self.get_object())

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Groups of user: %s') % self.get_object()
        }

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs['pk'])

    def left_list(self):
        return AssignRemoveView.generate_choices(
            Group.objects.exclude(user=self.get_object())
        )

    def right_list(self):
        return AssignRemoveView.generate_choices(
            Group.objects.filter(user=self.get_object())
        )

    def remove(self, item):
        item.user_set.remove(self.get_object())


class UserListView(SingleObjectListView):
    view_permission = permission_user_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'title': _('Users'),
        }

    def get_queryset(self):
        return get_user_model().objects.exclude(
            is_superuser=True
        ).exclude(is_staff=True).order_by('last_name', 'first_name')


def user_add(request):
    Permission.check_permissions(request.user, (permission_user_create,))

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_unusable_password()
            user.save()
            messages.success(
                request, _('User "%s" created successfully.') % user
            )
            return HttpResponseRedirect(
                reverse('user_management:user_set_password', args=(user.pk,))
            )
    else:
        form = UserForm()

    return render_to_response('appearance/generic_form.html', {
        'title': _('Create new user'),
        'form': form,
    }, context_instance=RequestContext(request))


def user_delete(request, user_id=None, user_id_list=None):
    Permission.check_permissions(request.user, (permission_user_delete,))
    post_action_redirect = None

    if user_id:
        users = get_user_model().objects.filter(pk=user_id)
        post_action_redirect = reverse('user_management:user_list')
    elif user_id_list:
        users = get_user_model().objects.filter(pk__in=user_id_list)

    if not users:
        messages.error(request, _('Must provide at least one user.'))
        return HttpResponseRedirect(
            request.META.get(
                'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
            )
        )

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        for user in users:
            try:
                if user.is_superuser or user.is_staff:
                    messages.error(
                        request,
                        _(
                            'Super user and staff user deleting is not '
                            'allowed, use the admin interface for these cases.'
                        )
                    )
                else:
                    user.delete()
                    messages.success(
                        request, _('User "%s" deleted successfully.') % user
                    )
            except Exception as exception:
                messages.error(
                    request, _('Error deleting user "%(user)s": %(error)s') % {
                        'user': user, 'error': exception
                    }
                )

        return HttpResponseRedirect(next)

    context = {
        'delete_view': True,
        'previous': previous,
        'next': next,
    }
    if users.count() == 1:
        context['object'] = users.first()
        context['title'] = _('Delete the user: %s?') % ', '.join([unicode(d) for d in users])
    elif len(users) > 1:
        context['title'] = _('Delete the users: %s?') % ', '.join([unicode(d) for d in users])

    return render_to_response(
        'appearance/generic_confirm.html', context,
        context_instance=RequestContext(request)
    )


def user_multiple_delete(request):
    return user_delete(
        request, user_id_list=request.GET.get(
            'id_list', request.POST.get('id_list', '')
        ).split(',')
    )


def user_set_password(request, user_id=None, user_id_list=None):
    Permission.check_permissions(request.user, (permission_user_edit,))
    post_action_redirect = None

    if user_id:
        users = get_user_model().objects.filter(pk=user_id)
        post_action_redirect = reverse('user_management:user_list')
    elif user_id_list:
        users = get_user_model().objects.filter(pk__in=user_id_list)

    if not users:
        messages.error(request, _('Must provide at least one user.'))
        return HttpResponseRedirect(
            request.META.get(
                'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
            )
        )

    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password_1 = form.cleaned_data['new_password_1']
            password_2 = form.cleaned_data['new_password_2']
            if password_1 != password_2:
                messages.error(
                    request, _('Passwords do not match, try again.')
                )
            else:
                for user in users:
                    try:
                        if user.is_superuser or user.is_staff:
                            messages.error(
                                request,
                                _(
                                    'Super user and staff user password '
                                    'reseting is not allowed, use the admin '
                                    'interface for these cases.'
                                )
                            )
                        else:
                            user.set_password(password_1)
                            user.save()
                            messages.success(
                                request, _(
                                    'Successfull password reset for user: %s.'
                                ) % user
                            )
                    except Exception as exception:
                        messages.error(
                            request, _(
                                'Error reseting password for user "%(user)s": %(error)s'
                            ) % {
                                'user': user, 'error': exception
                            }
                        )

                return HttpResponseRedirect(next)
    else:
        form = PasswordForm()

    context = {
        'next': next,
        'form': form,
    }

    if users.count() == 1:
        context['object'] = users.first()
        context['title'] = _('Reseting password for user: %s') % ', '.join([unicode(d) for d in users])
    elif len(users) > 1:
        context['title'] = _('Reseting password for users: %s') % ', '.join([unicode(d) for d in users])

    return render_to_response(
        'appearance/generic_form.html', context,
        context_instance=RequestContext(request)
    )


def user_multiple_set_password(request):
    return user_set_password(
        request, user_id_list=request.GET.get(
            'id_list', request.POST.get('id_list', '')
        ).split(',')
    )
