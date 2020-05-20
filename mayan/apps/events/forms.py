from django import forms
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext_lazy as _

from .models import EventSubscription, ObjectEventSubscription


class EventTypeUserRelationshipForm(forms.Form):
    namespace = forms.CharField(
        label=_('Namespace'), required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    label = forms.CharField(
        label=_('Label'), required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    subscription = forms.ChoiceField(
        label=_('Subscription'),
        widget=forms.RadioSelect(), choices=(
            ('none', _('No')),
            ('subscribed', _('Subscribed')),
        )
    )

    def __init__(self, *args, **kwargs):
        super(EventTypeUserRelationshipForm, self).__init__(
            *args, **kwargs
        )

        if 'stored_event_type' in self.initial:
            self.fields['namespace'].initial = self.initial['stored_event_type'].namespace
            self.fields['label'].initial = self.initial['stored_event_type'].label

            subscription = EventSubscription.objects.get_for(
                stored_event_type=self.initial['stored_event_type'],
                user=self.initial['user'],
            )

            if subscription.exists():
                self.fields['subscription'].initial = 'subscribed'
            else:
                self.fields['subscription'].initial = 'none'

    def save(self):
        subscription = EventSubscription.objects.get_for(
            stored_event_type=self.initial['stored_event_type'],
            user=self.initial['user'],
        )

        if self.cleaned_data['subscription'] == 'none':
            subscription.delete()
        elif self.cleaned_data['subscription'] == 'subscribed':
            if not subscription.exists():
                EventSubscription.objects.create_for(
                    stored_event_type=self.initial['stored_event_type'],
                    user=self.initial['user']
                )


EventTypeUserRelationshipFormSet = formset_factory(
    EventTypeUserRelationshipForm, extra=0
)


class ObjectEventTypeUserRelationshipForm(forms.Form):
    namespace = forms.CharField(
        label=_('Namespace'), required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    label = forms.CharField(
        label=_('Label'), required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    subscription = forms.ChoiceField(
        label=_('Subscription'),
        widget=forms.RadioSelect(), choices=(
            ('none', _('No')),
            ('subscribed', _('Subscribed')),
        )
    )

    def __init__(self, *args, **kwargs):
        super(ObjectEventTypeUserRelationshipForm, self).__init__(
            *args, **kwargs
        )

        self.fields['namespace'].initial = self.initial['stored_event_type'].namespace
        self.fields['label'].initial = self.initial['stored_event_type'].label

        subscription = ObjectEventSubscription.objects.get_for(
            obj=self.initial['object'],
            stored_event_type=self.initial['stored_event_type'],
            user=self.initial['user'],
        )

        if subscription.exists():
            self.fields['subscription'].initial = 'subscribed'
        else:
            self.fields['subscription'].initial = 'none'

    def save(self):
        subscription = ObjectEventSubscription.objects.get_for(
            obj=self.initial['object'],
            stored_event_type=self.initial['stored_event_type'],
            user=self.initial['user'],
        )

        if self.cleaned_data['subscription'] == 'none':
            subscription.delete()
        elif self.cleaned_data['subscription'] == 'subscribed':
            if not subscription.exists():
                ObjectEventSubscription.objects.create_for(
                    obj=self.initial['object'],
                    stored_event_type=self.initial['stored_event_type'],
                    user=self.initial['user']
                )


ObjectEventTypeUserRelationshipFormSet = formset_factory(
    ObjectEventTypeUserRelationshipForm, extra=0
)
