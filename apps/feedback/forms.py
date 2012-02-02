from __future__ import absolute_import

import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class FeedbackForm(forms.Form):
    attract = forms.CharField(
        widget=forms.widgets.Textarea(
            attrs={'rows': 2},
        ),
        label=_(u'What features of Mayan EDMS attracted you to start using it or consider using it?'),
        required=False
    )

    future = forms.CharField(
        widget=forms.widgets.Textarea(
            attrs={'rows': 2},
        ),
        label=_(u'What features would you like to see implemented in Mayan EDMS?'),
        required=False
    )

    deploy = forms.CharField(
        widget=forms.widgets.Textarea(
            attrs={'rows': 2},
        ),
        label=_(u'Could you tell us a bit about how you are deploying or plan to deploy Mayan EDMS (OS, webserver, cloud/local, hardware specs)?'),
        required=False
    )

    hardest = forms.CharField(
        widget=forms.widgets.Textarea(
            attrs={'rows': 2},
        ),
        label=_(u'What features of Mayan EDMS did you find hardest to understand or implement?'),
        required=False
    )

    support = forms.BooleanField(
        label=_(u'Would you be interested in purchasing paid support for Mayan EDMS?'),
        required=False
    )

    sell_support = forms.BooleanField(
        label=_(u'Are currently providing or planning to provide paid support for Mayan EDMS?'),
        required=False
    )
    
    hosted = forms.BooleanField(
        label=_(u'Would you be interested in a cloud hosted solution for Mayan EDMS?'),
        required=False
    )

    turn_key = forms.BooleanField(
        label=_(u'Would you be interested in a turn-key solution for Mayan EDMS that included a physical server appliance?'),
        required=False
    )

    name = forms.CharField(
        label=_(u'Your name:'),
        required=False
    )

    email = forms.CharField(
        label=_(u'Your email:'),
        required=False
    )
    
    company = forms.CharField(
        label=_(u'Company name:'),
        required=False
    )

    website = forms.CharField(
        label=_(u'Company website:'),
        required=False
    )

    use_info = forms.BooleanField(
        label=_(u'May we display your company name & logo in our website as a user of Mayan EDMS with a link back to your website?'),
        required=False
    )

    mailing_list = forms.BooleanField(
        label=_(u'May we keep your contact information to keep you up to date with developments or oferings related to Mayan EDMS?'),
        required=False
    )
