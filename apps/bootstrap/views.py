from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.files import File

from filetransfers.api import serve_file

from permissions.models import Permission

from .models import BootstrapSetup
from .classes import Cleanup, BootstrapModel
from .permissions import (PERMISSION_BOOTSTRAP_VIEW, PERMISSION_BOOTSTRAP_CREATE,
    PERMISSION_BOOTSTRAP_EDIT, PERMISSION_BOOTSTRAP_DELETE,
    PERMISSION_BOOTSTRAP_EXECUTE, PERMISSION_NUKE_DATABASE, PERMISSION_BOOTSTRAP_DUMP,
    PERMISSION_BOOTSTRAP_EXPORT, PERMISSION_BOOTSTRAP_IMPORT, PERMISSION_BOOTSTRAP_REPOSITORY_SYNC)
from .forms import (BootstrapSetupForm, BootstrapSetupForm_view, BootstrapSetupForm_dump,
    BootstrapSetupForm_edit, BootstrapFileImportForm, BootstrapURLImportForm)
from .exceptions import ExistingData, NotABootstrapSetup


def bootstrap_setup_list(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_BOOTSTRAP_VIEW])

    context = {
        'object_list': BootstrapSetup.objects.all(),
        'title': _(u'bootstrap setups'),
        'hide_link': True,
        'extra_columns': [
            {'name': _(u'description'), 'attribute': 'description'},
            {'name': _(u'type'), 'attribute': 'get_type_display'},
        ],
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def bootstrap_setup_create(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_BOOTSTRAP_CREATE])

    if request.method == 'POST':
        form = BootstrapSetupForm(request.POST)
        if form.is_valid():
            bootstrap = form.save()
            messages.success(request, _(u'Bootstrap setup created successfully'))
            return HttpResponseRedirect(reverse('bootstrap_setup_list'))
        else:
            messages.error(request, _(u'Error creating bootstrap setup.'))
    else:
        form = BootstrapSetupForm()

    return render_to_response('generic_form.html', {
        'title': _(u'create bootstrap'),
        'form': form,
    },
    context_instance=RequestContext(request))


def bootstrap_setup_edit(request, bootstrap_setup_pk):
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))

    bootstrap = get_object_or_404(BootstrapSetup, pk=bootstrap_setup_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_BOOTSTRAP_EDIT])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_BOOTSTRAP_EDIT, request.user, bootstrap)

    if request.method == 'POST':
        form = BootstrapSetupForm_edit(instance=bootstrap, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Bootstrap setup edited successfully'))
            return HttpResponseRedirect(previous)
        else:
            messages.error(request, _(u'Error editing bootstrap setup.'))
    else:
        form = BootstrapSetupForm_edit(instance=bootstrap)

    return render_to_response('generic_form.html', {
        'title': _(u'edit bootstrap setup: %s') % bootstrap,
        'form': form,
        'object': bootstrap,
        'previous': previous,
        'object_name': _(u'bootstrap setup'),
    },
    context_instance=RequestContext(request))


def bootstrap_setup_delete(request, bootstrap_setup_pk):
    bootstrap = get_object_or_404(BootstrapSetup, pk=bootstrap_setup_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_BOOTSTRAP_DELETE])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_BOOTSTRAP_DELETE, request.user, bootstrap)

    post_action_redirect = reverse('bootstrap_setup_list')

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            bootstrap.delete()
            messages.success(request, _(u'Bootstrap setup: %s deleted successfully.') % bootstrap)
        except Exception, e:
            messages.error(request, _(u'Bootstrap setup: %(bootstrap)s, delete error: %(error)s') % {
                'bootstrap': bootstrap, 'error': e})

        return HttpResponseRedirect(reverse('bootstrap_setup_list'))

    context = {
        'object_name': _(u'bootstrap setup'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'object': bootstrap,
        'title': _(u'Are you sure you with to delete the bootstrap setup: %s?') % bootstrap,
        'form_icon': 'lightning_delete.png',
    }

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def bootstrap_setup_view(request, bootstrap_setup_pk):
    bootstrap = get_object_or_404(BootstrapSetup, pk=bootstrap_setup_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_BOOTSTRAP_VIEW])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_BOOTSTRAP_VIEW, request.user, bootstrap)

    form = BootstrapSetupForm_view(instance=bootstrap)
    context = {
        'form': form,
        'object': bootstrap,
        'object_name': _(u'bootstrap setup'),
    }

    return render_to_response('generic_detail.html', context,
        context_instance=RequestContext(request))


def bootstrap_setup_execute(request, bootstrap_setup_pk):
    Permission.objects.check_permissions(request.user, [PERMISSION_BOOTSTRAP_EXECUTE])
    bootstrap_setup = get_object_or_404(BootstrapSetup, pk=bootstrap_setup_pk)

    post_action_redirect = reverse('bootstrap_setup_list')

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            bootstrap_setup.execute()
        except ExistingData:
            messages.error(request, _(u'Cannot execute bootstrap setup, there is existing data.  Erase all data and try again.'))
        except Exception, exc:
            messages.error(request, _(u'Error executing bootstrap setup; %s') % exc)
        else:
            messages.success(request, _(u'Bootstrap setup "%s" executed successfully.') % bootstrap_setup)
            return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'bootstrap setup'),
        'delete_view': False,
        'previous': previous,
        'next': next,
        'form_icon': 'lightning_go.png',
        'object': bootstrap_setup,
    }

    context['title'] = _(u'Are you sure you wish to execute the database bootstrap setup named: %s?') % bootstrap_setup

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def bootstrap_setup_dump(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_BOOTSTRAP_DUMP])

    if request.method == 'POST':
        form = BootstrapSetupForm_dump(request.POST)
        if form.is_valid():
            bootstrap = form.save(commit=False)
            try:
                bootstrap.fixture = BootstrapSetup.objects.dump(serialization_format=bootstrap.type)
            except Exception as exception:
                messages.error(request, _(u'Error dumping configuration into a bootstrap setup; %s') % exception)
                raise
            else:
                bootstrap.save()
                messages.success(request, _(u'Bootstrap setup created successfully.'))
                return HttpResponseRedirect(reverse('bootstrap_setup_list'))
    else:
        form = BootstrapSetupForm_dump()

    return render_to_response('generic_form.html', {
        'title': _(u'dump current configuration into a bootstrap setup'),
        'form': form,
    },
    context_instance=RequestContext(request))


def bootstrap_setup_export(request, bootstrap_setup_pk):
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))

    bootstrap = get_object_or_404(BootstrapSetup, pk=bootstrap_setup_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_BOOTSTRAP_EXPORT])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_BOOTSTRAP_EXPORT, request.user, bootstrap)
       
    return serve_file(
        request,
        bootstrap.as_file(),
        save_as=u'"%s"' % bootstrap.get_filename(),
        content_type='text/plain; charset=us-ascii'
    )


def bootstrap_setup_import_from_file(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_BOOTSTRAP_IMPORT])

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        form = BootstrapFileImportForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                BootstrapSetup.objects.import_from_file(request.FILES['file'])
                messages.success(request, _(u'Bootstrap setup imported successfully.'))
                return HttpResponseRedirect(reverse('bootstrap_setup_list'))
            except NotABootstrapSetup:
                messages.error(request, _(u'File is not a bootstrap setup.'))
            except Exception as exception:
                messages.error(request, _(u'Error importing bootstrap setup from file; %s.') % exception)
                return HttpResponseRedirect(previous)
    else:
        form = BootstrapFileImportForm()

    return render_to_response('generic_form.html', {
        'title': _(u'Import bootstrap setup from file'),
        'form_icon': 'folder.png',
        'form': form,
        'previous': previous,
    }, context_instance=RequestContext(request))


def bootstrap_setup_import_from_url(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_BOOTSTRAP_IMPORT])

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        form = BootstrapURLImportForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                BootstrapSetup.objects.import_from_url(form.cleaned_data['url'])
                messages.success(request, _(u'Bootstrap setup imported successfully.'))
                return HttpResponseRedirect(reverse('bootstrap_setup_list'))
            except NotABootstrapSetup:
                messages.error(request, _(u'Data from URL is not a bootstrap setup.'))
            except Exception as exception:
                messages.error(request, _(u'Error importing bootstrap setup from URL; %s.') % exception)
                return HttpResponseRedirect(previous)
    else:
        form = BootstrapURLImportForm()

    return render_to_response('generic_form.html', {
        'title': _(u'Import bootstrap setup from URL'),
        'form_icon': 'folder.png',
        'form': form,
        'previous': previous,
    }, context_instance=RequestContext(request))


def erase_database_view(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_NUKE_DATABASE])

    post_action_redirect = None

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            Cleanup.execute_all()
        except Exception, exc:
            messages.error(request, _(u'Error erasing database; %s') % exc)
        else:
            messages.success(request, _(u'Database erased successfully.'))
            return HttpResponseRedirect(next)

    context = {
        'delete_view': False,
        'previous': previous,
        'next': next,
        'form_icon': 'radioactivity.png',
    }

    context['title'] = _(u'Are you sure you wish to erase the entire database and document storage?')
    context['message'] = _(u'All documents, sources, metadata, metadata types, set, tags, indexes and logs will be lost irreversibly!')

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def bootstrap_setup_repository_sync(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_BOOTSTRAP_REPOSITORY_SYNC])
    
    post_action_redirect = reverse('bootstrap_setup_list')

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            BootstrapSetup.objects.repository_sync()
            messages.success(request, _(u'Bootstrap repository successfully synchronized.'))
        except Exception, e:
            messages.error(request, _(u'Bootstrap repository synchronization error: %(error)s') % {'error': e})

        return HttpResponseRedirect(reverse('bootstrap_setup_list'))

    context = {
        'previous': previous,
        'next': next,
        'title': _(u'Are you sure you wish to synchronize with the bootstrap repository?'),
        'form_icon': 'world.png',
    }

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))
