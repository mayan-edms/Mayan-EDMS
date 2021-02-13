from django.template import Library

from ..models import Announcement

register = Library()


@register.inclusion_tag('announcements/announcements.html')
def announcements():
    return {'announcements': Announcement.objects.get_for_now()}
