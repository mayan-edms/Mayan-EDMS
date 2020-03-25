from django.template import Library

from ..models import Message

register = Library()


@register.inclusion_tag('motd/messages.html')
def motd():
    return {'messages': Message.objects.get_for_now()}
