from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.conf import settings
from django.template.defaultfilters import force_escape

from documents.models import Document, RecentDocument
from permissions.api import check_permissions

from django_gpg.api import Key
from django_gpg.runtime import gpg
from django_gpg.exceptions import GPGVerificationError
from django_gpg import PERMISSION_DOCUMENT_VERIFY


def key_list(request, secret=True):
    if secret:
        object_list = Key.get_all(gpg, secret=True)
        title = _(u'Private key list')
    else:
        object_list = Key.get_all(gpg)
        title = _(u'Public key list')

    return render_to_response('key_list.html', {
        'object_list': object_list,
        'title': title,
    }, context_instance=RequestContext(request))


def key_delete(request, fingerprint, key_type):
    if request.method == 'POST':
        try:
            secret = key_type == 'sec'
            key = Key.get(gpg, fingerprint, secret=secret)
            gpg.delete_key(key)
            messages.success(request, _(u'Key: %s, deleted successfully.') % fingerprint)
            return HttpResponseRedirect(reverse('home_view'))
        except Exception, msg:
            messages.error(request, msg)
            return HttpResponseRedirect(reverse('home_view'))

    return render_to_response('generic_confirm.html', {
        'title': _(u'Delete key'),
        'message': _(u'Are you sure you wish to delete key:%s?  If you try to delete a public key that is part of a public/private pair the private key will be deleted as well.') % Key.get(gpg, fingerprint)
    }, context_instance=RequestContext(request))


def document_verify(request, document_pk):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VERIFY])
    document = get_object_or_404(Document, pk=document_pk)

    RecentDocument.objects.add_document_for_user(request.user, document)
    try:
        signature = gpg.verify_w_retry(document.open())
    except GPGVerificationError:
        signature = None

    signature_states = {
        'signature bad': {
            'text': _(u'Bad signature.'),
            'icon': 'cross.png'
        },
        None: {
            'text': _(u'Document not signed or invalid signature.'),
            'icon': 'cross.png'
        },
        'signature error': {
            'text': _(u'Signature error.'),
            'icon': 'cross.png'
        },
        'no public key': {
            'text': _(u'Document is signed but no public key is available for verification.'),
            'icon': 'user_silhouette.png'
        },
        'signature good': {
            'text': _(u'Document is signed, and signature is good.'),
            'icon': 'document_signature.png'
        },
        'signature valid': {
            'text': _(u'Document is signed with a valid signature.'),
            'icon': 'document_signature.png'
        },
    }    
    
    signature_state = signature_states.get(getattr(signature, 'status', None))
    
    widget = (u'<img style="vertical-align: middle;" src="%simages/icons/%s" />' % (settings.STATIC_URL, signature_state['icon']))
    paragraphs = [
        _(u'Signature status: %s %s') % (mark_safe(widget), signature_state['text']),
    ]

    if signature:
        paragraphs.extend(
            [
                _(u'Signature ID: %s') % signature.signature_id,
                _(u'Key ID: %s') % signature.key_id,
                _(u'Timestamp: %s') % datetime.fromtimestamp(int(signature.sig_timestamp)),
                _(u'Signee: %s') % force_escape(getattr(signature, 'username', u'')),
            ]
        )
    
    return render_to_response('generic_template.html', {
        'title': _(u'signature properties for: %s') % document,
        'object': document,
        'document': document,
        'paragraphs': paragraphs,
    }, context_instance=RequestContext(request))
