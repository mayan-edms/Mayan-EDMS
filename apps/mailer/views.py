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

from .permissions import PERMISSION_MAILING_LINK, PERMISSION_MAILING_SEND_DOCUMENT
from .forms import DocumentMailForm


def send_document_link(request, document_id=None, document_id_list=None, as_attachment=False):
    if document_id:
        documents = [get_object_or_404(Document, pk=document_id)]
    elif document_id_list:
        documents = [get_object_or_404(Document, pk=document_id) for document_id in document_id_list.split(',')]

    if as_attachment:
        permission = PERMISSION_MAILING_SEND_DOCUMENT
    else:
        permission = PERMISSION_MAILING_LINK

    try:
        Permission.objects.check_permissions(request.user, [permission])
    except PermissionDenied:
        documents = AccessEntry.objects.filter_objects_by_access(permission, request.user, documents)

    if not documents:
        messages.error(request, _(u'Must provide at least one document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    post_action_redirect = reverse('document_list_recent')

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', post_action_redirect)))

    for document in documents:
        RecentDocument.objects.add_document_for_user(request.user, document)

    if request.method == 'POST':
        form = DocumentMailForm(request.POST, as_attachment=as_attachment)
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
            if as_attachment:
                for document in documents:
                    descriptor = document.open()
                    email_msg.attach(document.filename, descriptor.read(), document.file_mimetype)
                    descriptor.close()

            try:
                email_msg.send()
            except Exception, exc:
                if as_attachment:
                    messages.error(request, _(u'Error sending document: %(document)s, via email; %(error)s.') % {
                        'document': document, 'error': exc})
                else:
                    messages.error(request, _(u'Error sending document link for document %(document)s; %(error)s.') % {
                        'document': document, 'error': exc})

            else:
                if as_attachment:
                    messages.success(request, _(u'Successfully sent document via email.'))
                else:
                    messages.success(request, _(u'Successfully sent document link via email.'))
                return HttpResponseRedirect(next)
    else:
        form = DocumentMailForm(as_attachment=as_attachment)

    context = {
        'form': form,
        'next': next,
        'submit_label': _(u'Send'),
        'submit_icon_famfam': 'email_go'
    }
    if len(documents) == 1:
        context['object'] = documents[0]
        if as_attachment:
            context['title'] = _(u'Email document: %s') % ', '.join([unicode(d) for d in documents])
        else:
            context['title'] = _(u'Email link for document: %s') % ', '.join([unicode(d) for d in documents])
    elif len(documents) > 1:
        if as_attachment:
            context['title'] = _(u'Email documents: %s') % ', '.join([unicode(d) for d in documents])
        else:
            context['title'] = _(u'Email links for documents: %s') % ', '.join([unicode(d) for d in documents])

    return render_to_response('generic_form.html', context,
        context_instance=RequestContext(request))
