from __future__ import absolute_import, unicode_literals

from json import dumps, loads

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import login, password_change
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import (
    ChoiceForm, EmailAuthenticationForm, LicenseForm, LocaleProfileForm,
    LocaleProfileForm_view, UserForm, UserForm_view
)
from .mixins import (
    ExtraContextMixin, ObjectListPermissionFilterMixin,
    ObjectPermissionCheckMixin, RedirectionMixin, ViewPermissionCheckMixin
)
from .settings import LOGIN_METHOD


def multi_object_action_view(request):
    """
    Proxy view called first when using a multi object action, which
    then redirects to the appropiate specialized view
    """

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse('main:home'))))

    action = request.GET.get('action', None)
    id_list = ','.join([key[3:] for key in request.GET.keys() if key.startswith('pk_')])
    items_property_list = [loads(key[11:]) for key in request.GET.keys() if key.startswith('properties_')]

    if not action:
        messages.error(request, _('No action selected.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main:home')))

    if not id_list and not items_property_list:
        messages.error(request, _('Must select at least one item.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main:home')))

    # Separate redirects to keep backwards compatibility with older
    # functions that don't expect a properties_list parameter
    if items_property_list:
        return HttpResponseRedirect('%s?%s' % (
            action,
            urlencode({'items_property_list': dumps(items_property_list), 'next': next}))
        )
    else:
        return HttpResponseRedirect('%s?%s' % (
            action,
            urlencode({'id_list': id_list, 'next': next}))
        )


def get_obj_from_content_type_string(string):
    model, pk = string.split(',')
    ct = ContentType.objects.get(model=model)
    return ct.get_object_for_this_type(pk=pk)


def assign_remove(request, left_list, right_list, add_method, remove_method, left_list_title=None, right_list_title=None, decode_content_type=False, extra_context=None, grouped=False):
    left_list_name = 'left_list'
    right_list_name = 'right_list'

    if request.method == 'POST':
        if '%s-submit' % left_list_name in request.POST.keys():
            unselected_list = ChoiceForm(request.POST,
                                         prefix=left_list_name,
                                         choices=left_list())
            if unselected_list.is_valid():
                for selection in unselected_list.cleaned_data['selection']:
                    if grouped:
                        flat_list = []
                        for group in left_list():
                            flat_list.extend(group[1])
                    else:
                        flat_list = left_list()

                    label = dict(flat_list)[selection]
                    if decode_content_type:
                        selection_obj = get_obj_from_content_type_string(selection)
                    else:
                        selection_obj = selection
                    try:
                        add_method(selection_obj)
                    except:
                        if settings.DEBUG:
                            raise
                        else:
                            messages.error(request, _('Unable to remove %(selection)s.') % {
                                'selection': label, 'right_list_title': right_list_title})

        elif '%s-submit' % right_list_name in request.POST.keys():
            selected_list = ChoiceForm(request.POST,
                                       prefix=right_list_name,
                                       choices=right_list())
            if selected_list.is_valid():
                for selection in selected_list.cleaned_data['selection']:
                    if grouped:
                        flat_list = []
                        for group in right_list():
                            flat_list.extend(group[1])
                    else:
                        flat_list = right_list()

                    label = dict(flat_list)[selection]
                    if decode_content_type:
                        selection = get_obj_from_content_type_string(selection)
                    try:
                        remove_method(selection)
                    except:
                        if settings.DEBUG:
                            raise
                        else:
                            messages.error(request, _('Unable to add %(selection)s.') % {
                                'selection': label, 'right_list_title': right_list_title})
    unselected_list = ChoiceForm(prefix=left_list_name, choices=left_list())
    selected_list = ChoiceForm(prefix=right_list_name, choices=right_list())

    context = {
        'subtemplates_list': [
            {
                'name': 'main/generic_form_subtemplate.html',
                'grid': 12,
                'context': {
                    'form': unselected_list,
                    'title': left_list_title or ' ',
                    'submit_label': _('Add'),
                    'submit_icon_famfam': 'add'
                }
            },
            {
                'name': 'main/generic_form_subtemplate.html',
                'grid': 12,
                'grid_clear': True,
                'context': {
                    'form': selected_list,
                    'title': right_list_title or ' ',
                    'submit_label': _('Remove'),
                    'submit_icon_famfam': 'delete'
                }
            },

        ],
    }
    if extra_context:
        context.update(extra_context)

    return render_to_response('main/generic_form.html', context,
                              context_instance=RequestContext(request))


def current_user_details(request):
    """
    Display the current user's details
    """
    form = UserForm_view(instance=request.user)

    return render_to_response(
        'main/generic_form.html', {
            'form': form,
            'title': _('Current user details'),
            'read_only': True,
        },
        context_instance=RequestContext(request))


def current_user_locale_profile_details(request):
    """
    Display the current user's locale profile details
    """
    form = LocaleProfileForm_view(instance=request.user.locale_profile)

    return render_to_response(
        'main/generic_form.html', {
            'form': form,
            'title': _('Current user locale profile details'),
            'read_only': True,
        },
        context_instance=RequestContext(request))


def current_user_edit(request):
    """
    Allow an user to edit his own details
    """

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse('common:current_user_details'))))

    if request.method == 'POST':
        form = UserForm(instance=request.user, data=request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exclude(pk=request.user.pk).count():
                messages.error(request, _('E-mail conflict, another user has that same email.'))
            else:
                form.save()
                messages.success(request, _('Current user\'s details updated.'))
                return HttpResponseRedirect(next)
    else:
        form = UserForm(instance=request.user)

    return render_to_response(
        'main/generic_form.html', {
            'form': form,
            'next': next,
            'title': _('Edit current user details'),
        },
        context_instance=RequestContext(request))


def current_user_locale_profile_edit(request):
    """
    Allow an user to edit his own locale profile
    """

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse('common:current_user_locale_profile_details'))))

    if request.method == 'POST':
        form = LocaleProfileForm(instance=request.user.locale_profile, data=request.POST)
        if form.is_valid():
            form.save()

            if hasattr(request, 'session'):
                request.session['django_language'] = form.cleaned_data['language']
                request.session['django_timezone'] = form.cleaned_data['timezone']
            else:
                request.set_cookie(settings.LANGUAGE_COOKIE_NAME, form.cleaned_data['language'])

            messages.success(request, _('Current user\'s locale profile details updated.'))
            return HttpResponseRedirect(next)
    else:
        form = LocaleProfileForm(instance=request.user.locale_profile)

    return render_to_response(
        'main/generic_form.html', {
            'form': form,
            'next': next,
            'title': _('Edit current user locale profile details'),
        },
        context_instance=RequestContext(request))


def login_view(request):
    """
    Control how the use is to be authenticated, options are 'email' and
    'username'
    """
    kwargs = {'template_name': 'main/login.html'}

    if LOGIN_METHOD == 'email':
        kwargs['authentication_form'] = EmailAuthenticationForm

    if not request.user.is_authenticated():
        context = {'web_theme_view_type': 'plain'}
    else:
        context = {}

    return login(request, extra_context=context, **kwargs)


def license_view(request):
    """
    Display the included LICENSE file from the about menu
    """
    form = LicenseForm()
    return render_to_response(
        'main/generic_detail.html', {
            'form': form,
            'title': _('License'),
        },
        context_instance=RequestContext(request))


def password_change_view(request):
    """
    Password change wrapper for better control
    """
    context = {'title': _('Current user password change')}

    return password_change(
        request,
        extra_context=context,
        template_name='main/password_change_form.html',
        post_change_redirect=reverse('common:password_change_done'),
    )


def password_change_done(request):
    """
    View called when the new user password has been accepted
    """

    messages.success(request, _('Your password has been successfully changed.'))
    return redirect('common:current_user_details')


class SingleObjectEditView(ViewPermissionCheckMixin, ObjectPermissionCheckMixin, ExtraContextMixin, RedirectionMixin, UpdateView):
    template_name = 'main/generic_form.html'

    def form_invalid(self, form):
        result = super(SingleObjectEditView, self).form_invalid(form)

        try:
            messages.error(self.request, _('Error saving %s details.') % self.extra_context['object_name'])
        except KeyError:
            messages.error(self.request, _('Error saving details.'))

        return result

    def form_valid(self, form):
        result = super(SingleObjectEditView, self).form_valid(form)

        try:
            messages.success(self.request, _('%s details saved successfully.') % self.extra_context['object_name'].capitalize())
        except KeyError:
            messages.success(self.request, _('Details saved successfully.'))

        return result


class SingleObjectCreateView(ViewPermissionCheckMixin, ExtraContextMixin, RedirectionMixin, CreateView):
    template_name = 'main/generic_form.html'

    def form_invalid(self, form):
        result = super(SingleObjectCreateView, self).form_invalid(form)

        try:
            messages.error(self.request, _('Error creating new %s.') % self.extra_context['object_name'])
        except KeyError:
            messages.error(self.request, _('Error creating object.'))

        return result

    def form_valid(self, form):
        result = super(SingleObjectCreateView, self).form_valid(form)
        try:
            messages.success(self.request, _('%s created successfully.') % self.extra_context['object_name'].capitalize())
        except KeyError:
            messages.success(self.request, _('New object created successfully.'))

        return result


class SingleObjectDeleteView(ViewPermissionCheckMixin, ObjectPermissionCheckMixin, ExtraContextMixin, RedirectionMixin, DeleteView):
    template_name = 'main/generic_confirm.html'

    def get_context_data(self, **kwargs):
        context = super(SingleObjectDeleteView, self).get_context_data(**kwargs)
        context.update({'delete_view': True})
        return context

    def delete(self, request, *args, **kwargs):
        try:
            result = super(SingleObjectDeleteView, self).delete(request, *args, **kwargs)
        except Exception as exception:
            try:
                messages.error(self.request, _('Error deleting %s.') % self.extra_context['object_name'])
            except KeyError:
                messages.error(self.request, _('Error deleting object.'))

            raise exception
        else:
            try:
                messages.success(self.request, _('%s deleted successfully.') % self.extra_context['object_name'].capitalize())
            except KeyError:
                messages.success(self.request, _('Object deleted successfully.'))

            return result


class SingleObjectListView(ViewPermissionCheckMixin, ObjectListPermissionFilterMixin, ExtraContextMixin, RedirectionMixin, ListView):
    template_name = 'main/generic_list.html'


class MultiFormView(FormView):
    prefixes = {}

    prefix = None

    def get_form_kwargs(self, form_name):
        kwargs = {}
        kwargs.update({'initial': self.get_initial(form_name)})
        kwargs.update({'prefix': self.get_prefix(form_name)})

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })

        return kwargs

    def _create_form(self, form_name, klass):
        form_kwargs = self.get_form_kwargs(form_name)
        form_create_method = 'create_%s_form' % form_name
        if hasattr(self, form_create_method):
            form = getattr(self, form_create_method)(**form_kwargs)
        else:
            form = klass(**form_kwargs)
        return form

    def get_forms(self, form_classes):
        return dict([(key, self._create_form(key, klass)) for key, klass in form_classes.items()])

    def get_initial(self, form_name):
        initial_method = 'get_%s_initial' % form_name
        if hasattr(self, initial_method):
            return getattr(self, initial_method)()
        else:
            return self.initial.copy()

    def get_prefix(self, form_name):
        return self.prefixes.get(form_name, self.prefix)

    def get(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        forms = self.get_forms(form_classes)
        return self.render_to_response(self.get_context_data(forms=forms))

    def forms_valid(self, forms):
        for form_name, form in forms.items():
            form_valid_method = '%s_form_valid' % form_name

            if hasattr(self, form_valid_method):
                return getattr(self, form_valid_method)(form)

        self.all_forms_valid(forms)

        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, forms):
        return self.render_to_response(self.get_context_data(forms=forms))

    def post(self, request, *args, **kwargs):
        form_classes = self.get_form_classes()
        forms = self.get_forms(form_classes)

        if all([form.is_valid() for form in forms.values()]):
            return self.forms_valid(forms)
        else:
            return self.forms_invalid(forms)
