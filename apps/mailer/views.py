from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template import Context, Template
from django.contrib.sites.models import Site

from documents.models import Document, RecentDocument
from permissions.models import Permission
from acls.models import AccessEntry

from .permissions import PERMISSION_MAILING_LINK
from .forms import DocumentMailForm


def send_document_link(request, document_id=None, document_id_list=None):
    if document_id:
        documents = [get_object_or_404(Document, pk=document_id)]
    elif document_id_list:
        documents = [get_object_or_404(Document, pk=document_id) for document_id in document_id_list.split(',')]

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_MAILING_LINK])
    except PermissionDenied:
        documents = AccessEntry.objects.filter_objects_by_access(PERMISSION_MAILING_LINK, request.user, documents)

    if not documents:
        messages.error(request, _(u'Must provide at least one document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    post_action_redirect = reverse('document_list_recent')

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', post_action_redirect)))

    for document in documents:
        RecentDocument.objects.add_document_for_user(request.user, document)

    if request.method == 'POST':
        form = DocumentMailForm(request.POST)
        if form.is_valid():
            context = Context({
                'link': 'http://%s%s' % (Site.objects.get_current().domain, reverse('document_view_simple', args=[document.pk])),
                'document': document
            })
            body_template = Template(form.cleaned_data['body'])
            body_html_content = body_template.render(context)
            body_text_content = strip_tags(body_html_content)

            subject_template = Template(form.cleaned_data['subject'])
            subject_text = strip_tags(subject_template.render(context))

            email_msg = EmailMultiAlternatives(subject_text, body_text_content, request.user.email, [form.cleaned_data['email']])
            email_msg.attach_alternative(body_html_content, 'text/html')
            try:
                email_msg.send()
            except Exception, exc:
                messages.error(request, _(u'Error sending document link for document %(document)s; %(error)s.') % {
                    'document': document, 'error': exc})
            else:
                messages.success(request, _(u'Successfully sent document link via email.'))
                return HttpResponseRedirect(next)
    else:
        form = DocumentMailForm()

    context = {
        'form': form,
        'next': next,
        'submit_label': _(u'send'),
    }
    if len(documents) == 1:
        context['object'] = documents[0]
        context['title'] = _(u'Email link for document: %s') % ', '.join([unicode(d) for d in documents])
    elif len(documents) > 1:
        context['title'] = _(u'Email links for documents: %s') % ', '.join([unicode(d) for d in documents])

    return render_to_response('generic_form.html', context,
        context_instance=RequestContext(request))
