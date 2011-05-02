from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_list
from django.core.urlresolvers import reverse
from django.views.generic.create_update import create_object, delete_object, update_object
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from permissions.api import check_permissions

from user_management import PERMISSION_USER_VIEW, \
    PERMISSION_USER_EDIT, PERMISSION_USER_CREATE, \
    PERMISSION_USER_DELETE
from user_management.forms import UserForm

def user_list(request):
    check_permissions(request.user, 'user_management', [PERMISSION_USER_VIEW])

    return object_list(
        request,
        queryset=User.objects.all(),
        template_name='generic_list.html',
        extra_context={
            'title': _(u'users'),
            'hide_link': True,
            'extra_columns': [
                {
                    'name': _(u'full name'),
                    'attribute': 'get_full_name'
                },
                {
                    'name': _(u'active'),
                    'attribute': 'is_active'
                }
                
            ],
            'multi_select_as_buttons': True,
        },
    )


def user_edit(request, user_id):
    check_permissions(request.user, 'user_management', [PERMISSION_USER_EDIT])
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        form = UserForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _(u'User "%s" updated successfully.') % user)
            return HttpResponseRedirect(reverse('user_list'))
    else:
        form = UserForm(instance=user)

    return render_to_response('generic_form.html', {
        'title': _(u'edit user: %s') % user,
        'form': form,
        'object': user,
    },
    context_instance=RequestContext(request))


def user_add(request):
    check_permissions(request.user, 'user_management', [PERMISSION_USER_CREATE])
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, _(u'User "%s" created successfully.') % user)
            return HttpResponseRedirect(reverse('user_list'))
    else:
        form = UserForm()

    return render_to_response('generic_form.html', {
        'title': _(u'create new user'),
        'form': form,
    },
    context_instance=RequestContext(request))


def user_delete(request, user_id=None, user_id_list=None):
    check_permissions(request.user, 'users', [PERMISSION_USER_DELETE])
    post_action_redirect = None

    if user_id:
        users = [get_object_or_404(User, pk=user_id)]
        post_action_redirect = reverse('user_list')
    elif user_id_list:
        users = [get_object_or_404(User, pk=user_id) for user_id in user_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one user.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for user in users:
            try:
                user.delete()
                messages.success(request, _(u'User "%s" deleted successfully.') % user)
            except Exception, e:
                messages.error(request, _(u'Error deleting user "%(user)s": %(error)s') % {
                    'user': user, 'error': e
                })

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'user'),
        'delete_view': True,
        'previous': previous,
        'next': next,
    }
    if len(users) == 1:
        context['object'] = users[0]
        context['title'] = _(u'Are you sure you wish to delete the user: %s?') % ', '.join([unicode(d) for d in users])
    elif len(users) > 1:
        context['title'] = _(u'Are you sure you wish to delete the users: %s?') % ', '.join([unicode(d) for d in users])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def user_multiple_delete(request):
    return user_delete(
        request, user_id_list=request.GET.get('id_list', [])
    )
