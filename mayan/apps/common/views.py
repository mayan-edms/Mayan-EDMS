from __future__ import absolute_import, unicode_literals

from json import dumps, loads

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone, translation
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from documents.search import document_search

from .classes import MissingItem
from .forms import (
    ChoiceForm, LicenseForm, LocaleProfileForm, LocaleProfileForm_view,
    UserForm, UserForm_view
)
from .menus import menu_tools, menu_setup
from .mixins import (
    ExtraContextMixin, ObjectListPermissionFilterMixin,
    ObjectPermissionCheckMixin, RedirectionMixin, ViewPermissionCheckMixin
)


class AssignRemoveView(ViewPermissionCheckMixin, ObjectPermissionCheckMixin, TemplateView):
    decode_content_type = False
    extra_context = None
    grouped = False
    left_list_title = None
    right_list_title = None
    template_name = 'appearance/generic_form.html'

    LEFT_LIST_NAME = 'left_list'
    RIGHT_LIST_NAME = 'right_list'

    @staticmethod
    def generate_choices(choices):
        results = []
        for choice in choices:
            ct = ContentType.objects.get_for_model(choice)
            if isinstance(choice, User):
                label = choice.get_full_name() if choice.get_full_name() else choice
            else:
                label = unicode(choice)

            results.append(('%s,%s' % (ct.model, choice.pk), '%s' % (label)))

        # Sort results by the label not the key value
        return sorted(results, key=lambda x: x[1])

    def left_list(self):
        # Subclass must override
        raise NotImplementedError

    def right_list(self):
        # Subclass must override
        raise NotImplementedError

    def add(self, item):
        # Subclass must override
        raise NotImplementedError

    def remove(self, item):
        # Subclass must override
        raise NotImplementedError

    def get(self, request, *args, **kwargs):
        self.unselected_list = ChoiceForm(prefix=self.LEFT_LIST_NAME, choices=self.left_list())
        self.selected_list = ChoiceForm(prefix=self.RIGHT_LIST_NAME, choices=self.right_list())
        return self.render_to_response(self.get_context_data())

    def process_form(self, prefix, items_function, action_function):
        if '%s-submit' % prefix in self.request.POST.keys():
            form = ChoiceForm(
                self.request.POST, prefix=prefix,
                choices=items_function()
            )

            if form.is_valid():
                for selection in form.cleaned_data['selection']:
                    if self.grouped:
                        flat_list = []
                        for group in items_function():
                            flat_list.extend(group[1])
                    else:
                        flat_list = items_function()

                    label = dict(flat_list)[selection]
                    if self.decode_content_type:
                        model, pk = selection.split(',')
                        selection_obj = ContentType.objects.get(model=model).get_object_for_this_type(pk=pk)
                    else:
                        selection_obj = selection

                    try:
                        action_function(selection_obj)
                    except:
                        if settings.DEBUG:
                            raise
                        else:
                            messages.error(self.request, _('Unable to transfer selection: %s.') % label)

    def post(self, request, *args, **kwargs):
        self.process_form(prefix=self.LEFT_LIST_NAME, items_function=self.left_list, action_function=self.add)
        self.process_form(prefix=self.RIGHT_LIST_NAME, items_function=self.right_list, action_function=self.remove)
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(AssignRemoveView, self).get_context_data(**kwargs)
        data.update({
            'subtemplates_list': [
                {
                    'name': 'appearance/generic_form_subtemplate.html',
                    'column_class': 'col-xs-12 col-sm-6 col-md-6 col-lg-6',
                    'context': {
                        'form': self.unselected_list,
                        'title': self.left_list_title or ' ',
                        'submit_label': _('Add'),
                        'submit_icon': 'fa fa-plus',
                        'hide_labels': True,
                    }
                },
                {
                    'name': 'appearance/generic_form_subtemplate.html',
                    'column_class': 'col-xs-12 col-sm-6 col-md-6 col-lg-6',
                    'context': {
                        'form': self.selected_list,
                        'title': self.right_list_title or ' ',
                        'submit_label': _('Remove'),
                        'submit_icon': 'fa fa-minus',
                        'hide_labels': True,
                    }
                },

            ],
        })
        return data


class AboutView(TemplateView):
    template_name = 'appearance/about.html'


class ConfirmView(ObjectListPermissionFilterMixin, ViewPermissionCheckMixin, ExtraContextMixin, RedirectionMixin, TemplateView):
    template_name = 'appearance/generic_confirm.html'


class CurrentUserDetailsView(TemplateView):
    template_name = 'appearance/generic_form.html'

    def get_context_data(self, **kwargs):
        data = super(CurrentUserDetailsView, self).get_context_data(**kwargs)
        data.update({
            'form': UserForm_view(instance=self.request.user),
            'read_only': True,
            'title': _('Current user details'),
        })
        return data


class CurrentUserLocaleProfileDetailsView(TemplateView):
    template_name = 'appearance/generic_form.html'

    def get_context_data(self, **kwargs):
        data = super(CurrentUserLocaleProfileDetailsView, self).get_context_data(**kwargs)
        data.update({
            'form': LocaleProfileForm_view(instance=self.request.user.locale_profile),
            'read_only': True,
            'title': _('Current user locale profile details'),
        })
        return data


class HomeView(TemplateView):
    template_name = 'appearance/home.html'

    def get_context_data(self, **kwargs):
        data = super(HomeView, self).get_context_data(**kwargs)
        data.update({
            'hide_links': True,
            'search_results_limit': 100,
            'search_terms': self.request.GET.get('q'),
            'missing_list': [item for item in MissingItem.get_all() if item.condition()],
        })
        return data

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        queryset, ids, timedelta = document_search.search(request.GET, request.user)

        # Update the context with the search results
        context.update({
            'object_list': queryset,
            'time_delta': timedelta,
            'title': _('Results'),
        })

        return self.render_to_response(context)


class LicenseView(ExtraContextMixin, TemplateView):
    extra_context = {
        'form': LicenseForm(),
        'read_only': True,
        'title': _('License'),
    }
    template_name = 'appearance/generic_form.html'


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


# TODO: check/test if ViewPermissionCheckMixin, ObjectPermissionCheckMixin are
# in the right MRO
class SingleObjectEditView(ViewPermissionCheckMixin, ObjectPermissionCheckMixin, ExtraContextMixin, RedirectionMixin, UpdateView):
    template_name = 'appearance/generic_form.html'

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
    template_name = 'appearance/generic_form.html'

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
    template_name = 'appearance/generic_confirm.html'

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
    template_name = 'appearance/generic_list.html'


class ParentChildListView(ViewPermissionCheckMixin, ObjectPermissionCheckMixin, ExtraContextMixin, ListView, SingleObjectMixin):
    parent_model = None
    parent_queryset = None
    template_name = 'appearance/generic_list.html'

    def get(self, request, *args, **kwargs):
        # Parent
        self.object = self.get_object()

        # Children
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if (self.get_paginate_by(self.object_list) is not None
                    and hasattr(self.object_list, 'exists')):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.")
                              % {'class_name': self.__class__.__name__})

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_parent_queryset()
        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})
        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get_parent_queryset(self):
        """
        Return the `QuerySet` that will be used to look up the object.
        Note that this method is called by the default implementation of
        `get_object` and may not be called if `get_object` is overridden.
        """
        if self.parent_queryset is None:
            if self.parent_model:
                return self.model._default_manager.all()
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.parent_model, %(cls)s.parent_queryset, or override "
                    "%(cls)s.get_parent_queryset()." % {
                        'cls': self.__class__.__name__
                    }
                )
        return self.parent_queryset.all()

    def get_queryset(self):
        raise NotImplementedError


class SetupListView(TemplateView):
    template_name = 'appearance/generic_list_horizontal.html'

    def get_context_data(self, **kwargs):
        data = super(SetupListView, self).get_context_data(**kwargs)
        data.update({
            'resolved_links': menu_setup.resolve(context=RequestContext(self.request)),
            'title': _('Setup items'),
        })
        return data


class SimpleView(ViewPermissionCheckMixin, ExtraContextMixin, TemplateView):
    pass


class ToolsListView(SimpleView):
    template_name = 'appearance/generic_list_horizontal.html'

    def get_menu_links(self):
        return menu_tools.resolve(context=RequestContext(self.request))

    def get_extra_context(self):
        return {
            'resolved_links': self.get_menu_links(),
            'title': _('Tools'),
        }


def multi_object_action_view(request):
    """
    Proxy view called first when using a multi object action, which
    then redirects to the appropiate specialized view
    """

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    action = request.GET.get('action', None)
    id_list = ','.join([key[3:] for key in request.GET.keys() if key.startswith('pk_')])
    items_property_list = [loads(key[11:]) for key in request.GET.keys() if key.startswith('properties_')]

    if not action:
        messages.error(request, _('No action selected.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)))

    if not id_list and not items_property_list:
        messages.error(request, _('Must select at least one item.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)))

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
        'appearance/generic_form.html', {
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

            timezone.activate(form.cleaned_data['timezone'])
            translation.activate(form.cleaned_data['language'])

            if hasattr(request, 'session'):
                request.session[translation.LANGUAGE_SESSION_KEY] = form.cleaned_data['language']
                request.session['django_timezone'] = form.cleaned_data['timezone']
            else:
                request.set_cookie(settings.LANGUAGE_COOKIE_NAME, form.cleaned_data['language'])

            messages.success(request, _('Current user\'s locale profile details updated.'))
            return HttpResponseRedirect(next)
    else:
        form = LocaleProfileForm(instance=request.user.locale_profile)

    return render_to_response(
        'appearance/generic_form.html', {
            'form': form,
            'next': next,
            'title': _('Edit current user locale profile details'),
        },
        context_instance=RequestContext(request))
