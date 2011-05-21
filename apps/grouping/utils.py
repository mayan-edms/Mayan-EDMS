from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.core.urlresolvers import reverse

from grouping.models import DocumentGroup
from grouping.conf.settings import SHOW_EMPTY_GROUPS
from grouping.forms import DocumentDataGroupForm
from grouping import document_group_link


def get_document_group_subtemplate(request, document):
    document_groups, errors = DocumentGroup.objects.get_groups_for(document)
    if (request.user.is_staff or request.user.is_superuser) and errors:
        for error in errors:
            messages.warning(request, _(u'Document group query error: %s' % error))

    if not SHOW_EMPTY_GROUPS:
        #If GROUP_SHOW_EMPTY is False, remove empty groups from
        #dictionary
        document_groups = dict([(group, data) for group, data in document_groups.items() if data['documents']])

    if document_groups:
        return {
            'name': 'generic_form_subtemplate.html',
            'context': {
                'title': _(u'document groups (%s)') % len(document_groups.keys()),
                'form': DocumentDataGroupForm(
                    groups=document_groups, current_document=document,
                    links=[document_group_link]
                ),
                'form_action': reverse('document_group_action'),
                'submit_method': 'GET',
            }
        }
    else:
        return None
