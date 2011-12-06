from datetime import datetime
import logging

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
from common.utils import pretty_size, parse_range, urlquote, \
    return_diff, encapsulate
from filetransfers.api import serve_file
   
from django_gpg.api import Key, SIGNATURE_STATES
from django_gpg.runtime import gpg
from django_gpg.exceptions import GPGVerificationError, KeyFetchingError
from django_gpg import (PERMISSION_DOCUMENT_VERIFY, PERMISSION_KEY_VIEW,
    PERMISSION_KEY_DELETE, PERMISSION_KEYSERVER_QUERY, 
    PERMISSION_KEY_RECEIVE, PERMISSION_SIGNATURE_UPLOAD,
    PERMISSION_SIGNATURE_DOWNLOAD)
from django_gpg.forms import KeySearchForm, DetachedSignatureForm

logger = logging.getLogger(__name__)


def key_receive(request, key_id):
    check_permissions(request.user, [PERMISSION_KEY_RECEIVE])
    
    post_action_redirect = None
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            term = request.GET.get('term')
            results = gpg.query(term)
            keys_dict = dict([(key.keyid, key) for key in results])
            key = gpg.import_key(keys_dict[key_id].key)
            messages.success(request, _(u'Key: %s, imported successfully.') % key)
            return HttpResponseRedirect(next)
        except (KeyFetchingError, KeyError, TypeError):
            messages.error(request, _(u'Unable to import key id: %s') % key_id)
            return HttpResponseRedirect(previous)

    return render_to_response('generic_confirm.html', {
        'title': _(u'Import key'),
        'message': _(u'Are you sure you wish to import key id: %s?') % key_id,
        'form_icon': 'key_add.png',
        'next': next,
        'previous': previous,
        'submit_method': 'GET',
        
    }, context_instance=RequestContext(request))
    

def key_list(request, secret=True):
    check_permissions(request.user, [PERMISSION_KEY_VIEW])
    
    if secret:
        object_list = Key.get_all(gpg, secret=True)
        title = _(u'private keys')
    else:
        object_list = Key.get_all(gpg)
        title = _(u'public keys')

    return render_to_response('generic_list.html', {
        'object_list': object_list,
        'title': title,
        'hide_object': True,
        'extra_columns': [
            {
                'name': _(u'Key ID'),
                'attribute': 'key_id',
            },
            {
                'name': _(u'Owner'),
                'attribute': encapsulate(lambda x: u', '.join(x.uids)),
            },
        ]
    }, context_instance=RequestContext(request))


def key_delete(request, fingerprint, key_type):
    check_permissions(request.user, [PERMISSION_KEY_DELETE])
    
    secret = key_type == 'sec'
    key = Key.get(gpg, fingerprint, secret=secret)

    post_action_redirect = None
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            gpg.delete_key(key)
            messages.success(request, _(u'Key: %s, deleted successfully.') % fingerprint)
            return HttpResponseRedirect(next)
        except Exception, msg:
            messages.error(request, msg)
            return HttpResponseRedirect(previous)

    return render_to_response('generic_confirm.html', {
        'title': _(u'Delete key'),
        'delete_view': True,
        'message': _(u'Are you sure you wish to delete key: %s?  If you try to delete a public key that is part of a public/private pair the private key will be deleted as well.') % key,
        'form_icon': 'key_delete.png',
        'next': next,
        'previous': previous,
    }, context_instance=RequestContext(request))


def key_query(request):
    check_permissions(request.user, [PERMISSION_KEYSERVER_QUERY])
    
    subtemplates_list = []
    term = request.GET.get('term')

    form = KeySearchForm(initial={'term': term})
    subtemplates_list.append(
        {
            'name': 'generic_form_subtemplate.html',
            'context': {
                'title': _(u'Query key server'),
                'form': form,
                'submit_method': 'GET',
            },
        }
    )        
    
    if term:
        results = gpg.query(term)
        subtemplates_list.append(
            {
                'name': 'generic_list_subtemplate.html',
                'context': {
                    'title': _(u'results'),
                    'object_list': results,
                    'hide_object': True,
                    'extra_columns': [
                        {
                            'name': _(u'ID'),
                            'attribute': 'keyid',
                        },
                        {
                            'name': _(u'type'),
                            'attribute': 'algo',
                        },
                        {
                            'name': _(u'creation date'),
                            'attribute': 'creation_date',
                        },                        
                        {
                            'name': _(u'disabled'),
                            'attribute': 'disabled',
                        },                        
                        {
                            'name': _(u'expiration date'),
                            'attribute': 'expiration_date',
                        },     
                        {
                            'name': _(u'expired'),
                            'attribute': 'expired',
                        },     
                        {
                            'name': _(u'length'),
                            'attribute': 'key_length',
                        },     
                        {
                            'name': _(u'revoked'),
                            'attribute': 'revoked',
                        },     
                        
                        {
                            'name': _(u'Identifies'),
                            'attribute': encapsulate(lambda x: u', '.join([identity.uid for identity in x.identities])),
                        },
                    ]                    
                },
            }
        )  

    return render_to_response('generic_form.html', {
        'subtemplates_list': subtemplates_list,
    }, context_instance=RequestContext(request))
    

def document_verify(request, document_pk):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VERIFY])
    document = get_object_or_404(Document, pk=document_pk)

    RecentDocument.objects.add_document_for_user(request.user, document)
   
    signature = document.verify_signature()
    
    signature_state = SIGNATURE_STATES.get(getattr(signature, 'status', None))
    
    widget = (u'<img style="vertical-align: middle;" src="%simages/icons/%s" />' % (settings.STATIC_URL, signature_state['icon']))
    paragraphs = [
        _(u'Signature status: %(widget)s %(text)s') % {
            'widget': mark_safe(widget),
            'text': signature_state['text']
        },
    ]

    if document.signature_state:
        signature_type = _(u'embedded')
    else:
        signature_type = _(u'detached')

    if signature:
        paragraphs.extend(
            [
                _(u'Signature ID: %s') % signature.signature_id,
                _(u'Signature type: %s') % signature_type,
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
    
    
def document_signature_upload(request, document_pk):
    check_permissions(request.user, [PERMISSION_SIGNATURE_UPLOAD])
    document = get_object_or_404(Document, pk=document_pk)

    RecentDocument.objects.add_document_for_user(request.user, document)
        
    post_action_redirect = None
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        form = DetachedSignatureForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                document.add_detached_signature(request.FILES['file'])
                messages.success(request, _(u'Detached signature uploaded successfully.'))
                return HttpResponseRedirect(next)
            except Exception, msg:
                messages.error(request, msg)
                return HttpResponseRedirect(previous)
    else:
        form = DetachedSignatureForm()

    return render_to_response('generic_form.html', {
        'title': _(u'Upload detached signature for: %s') % document,
        'form_icon': 'key_delete.png',
        'next': next,
        'form': form,
        'previous': previous,
        'object': document,
    }, context_instance=RequestContext(request))
    
    
def document_signature_download(request, document_pk):
    check_permissions(request.user, [PERMISSION_SIGNATURE_DOWNLOAD])
    document = get_object_or_404(Document, pk=document_pk)
        
    try:
        if document.has_detached_signature():
            signature = document.detached_signature()
            return serve_file(
                request,
                signature,
                save_as=u'"%s.sig"' % document.filename,
                content_type=u'application/octet-stream'
            )
    except Exception, e:
        messages.error(request, e)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
