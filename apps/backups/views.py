from __future__ import absolute_import

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _

from common.utils import encapsulate
from permissions.models import Permission

#from .classes import AppBackup
#from .forms import BackupJobForm
#from .models import App#, BackupJob
from .permissions import PERMISSION_BACKUP_JOB_VIEW, PERMISSION_BACKUP_JOB_CREATE, PERMISSION_BACKUP_JOB_EDIT


def backup_job_list(request):
    pre_object_list = BackupJob.objects.all()

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_BACKUP_JOB_VIEW])
    except PermissionDenied:
        # If user doesn't have global permission, get a list of backup jobs
        # for which he/she does have access use it to filter the
        # provided object_list
        final_object_list = AccessEntry.objects.filter_objects_by_access(PERMISSION_BACKUP_JOB_VIEW, request.user, pre_object_list)
    else:
        final_object_list = pre_object_list

    context = {
        'object_list': final_object_list,
        'title': _(u'backup jobs'),
        'hide_link': True,
        #'extra_columns': [
        #    {'name': _(u'info'), 'attribute': 'info'},
        #],
    }
    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def backup_job_create(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_BACKUP_JOB_CREATE])

    if request.method == 'POST':
        form = BackupJobForm(data=request.POST)
        if form.is_valid():
            try:
                backup_job = form.save()
            except Exception, exc:
                messages.error(request, _(u'Error creating backup job; %s') % exc)
            else:
                messages.success(request, _(u'Backup job "%s" created successfully.') % backup_job)
                return HttpResponseRedirect(reverse('backup_job_list'))
    else:
        form = BackupJobForm()

    return render_to_response('generic_form.html', {
        'form': form,
        'title': _(u'Create backup job')
    }, context_instance=RequestContext(request))
    

def backup_job_edit(request, backup_job_pk):
    backup_job = get_object_or_404(BackupJob, pk=backup_job_pk)
    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_BACKUP_JOB_EDIT])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_BACKUP_JOB_EDIT, request.user, backup_job)

    if request.method == 'POST':
        form = BackupJobForm(data=request.POST, instance=backup_job)
        if form.is_valid():
            try:
                backup_job = form.save()
            except Exception, exc:
                messages.error(request, _(u'Error editing backup job; %s') % exc)
            else:
                messages.success(request, _(u'Backup job "%s" edited successfully.') % backup_job)
                return HttpResponseRedirect(reverse('backup_job_list'))
    else:
        form = BackupJobForm(instance=backup_job)

    return render_to_response('generic_form.html', {
        'form': form,
        'object': backup_job,
        'title': _(u'Edit backup job: %s') % backup_job
    }, context_instance=RequestContext(request))


def backup_job_test(request, backup_job_pk):
    backup_job = get_object_or_404(BackupJob, pk=backup_job_pk)
    #try:
    #    Permission.objects.check_permissions(request.user, [PERMISSION_BACKUP_JOB_EDIT])
    #except PermissionDenied:
    #    AccessEntry.objects.check_access(PERMISSION_BACKUP_JOB_EDIT, request.user, backup_job)

    try:
        backup_job.backup(dry_run=True)
    except Exception, exc:
        if settings.DEBUG:
            raise
        else:
            messages.error(request, _(u'Error testing backup job; %s') % exc)
            return HttpResponseRedirect(reverse('backup_job_list'))
    else:
        messages.success(request, _(u'Test for backup job "%s" finished successfully.') % backup_job)
        return HttpResponseRedirect(reverse('backup_job_list'))


def backup_view(request):
    #Permission.objects.check_permissions(request.user, [])

    context = {
        'object_list': AppBackup.get_all(),
        'title': _(u'registered apps for backup'),
        'hide_link': True,
        'extra_columns': [
            {'name': _(u'info'), 'attribute': 'info'},
        ],
    }
    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))
