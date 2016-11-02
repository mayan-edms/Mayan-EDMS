from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib import messages
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, RequestContext, Template
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessControlList
from common.generics import SingleObjectListView
from documents.models import Document

from .forms import DocumentMailForm
from .models import LogEntry
from .permissions import (
    permission_mailing_link, permission_mailing_send_document,
    permission_view_error_log
)
from .tasks import task_send_document


class LogEntryListView(SingleObjectListView):
    extra_context = {
        'hide_object': True,
        'title': _('Document mailing error log'),
    }
    model = LogEntry
    view_permission = permission_view_error_log


def send_document_link(request, document_id=None, document_id_list=None, as_attachment=False):
    if document_id:
        documents = Document.objects.filter(pk=document_id)
    elif document_id_list:
        documents = Document.objects.filter(pk__in=document_id_list)

    if as_attachment:
        permission = permission_mailing_send_document
    else:
        permission = permission_mailing_link

    documents = AccessControlList.objects.filter_by_access(
        permission, request.user, queryset=documents
    )

    if not documents:
        messages.error(request, _('Must provide at least one document.'))
        return HttpResponseRedirect(
            request.META.get(
                'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
            )
        )

    post_action_redirect = reverse('documents:document_list_recent')

    next = request.POST.get(
        'next', request.GET.get(
            'next', request.META.get('HTTP_REFERER', post_action_redirect)
        )
    )

    for document in documents:
        document.add_as_recent_document_for_user(request.user)

    if request.method == 'POST':
        form = DocumentMailForm(request.POST, as_attachment=as_attachment)
        if form.is_valid():

            for document in documents:
                context = Context({
                    'link': 'http://%s%s' % (
                        Site.objects.get_current().domain,
                        document.get_absolute_url()
                    ),
                    'document': document
                })
                body_template = Template(form.cleaned_data['body'])
                body_html_content = body_template.render(context)
                body_text_content = strip_tags(body_html_content)

                subject_template = Template(form.cleaned_data['subject'])
                subject_text = strip_tags(subject_template.render(context))

                task_send_document.apply_async(
                    args=(
                        subject_text, body_text_content, request.user.email,
                        form.cleaned_data['email']
                    ), kwargs={
                        'document_id': document.pk,
                        'as_attachment': as_attachment
                    }
                )

            # TODO: Pluralize
            messages.success(
                request, _('Successfully queued for delivery via email.')
            )
            return HttpResponseRedirect(next)
    else:
        form = DocumentMailForm(as_attachment=as_attachment)

    context = {
        'form': form,
        'next': next,
        'submit_label': _('Send'),
        'submit_icon': 'fa fa-envelope'
    }
    if documents.count() == 1:
        context['object'] = documents.first()
        if as_attachment:
            context['title'] = _('Email document: %s') % ', '.join([unicode(d) for d in documents])
        else:
            context['title'] = _('Email link for document: %s') % ', '.join([unicode(d) for d in documents])
    elif documents.count() > 1:
        if as_attachment:
            context['title'] = _('Email documents: %s') % ', '.join([unicode(d) for d in documents])
        else:
            context['title'] = _('Email links for documents: %s') % ', '.join([unicode(d) for d in documents])

    return render_to_response(
        'appearance/generic_form.html', context,
        context_instance=RequestContext(request)
    )
