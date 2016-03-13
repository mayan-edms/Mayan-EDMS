from __future__ import unicode_literals

from django.template import Library

from ..models import MessageOfTheDay

register = Library()


@register.inclusion_tag('motd/messages.html')
def motd():
    return {'messages': MessageOfTheDay.objects.get_for_now()}
