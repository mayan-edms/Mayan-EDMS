from django.template import Library

register = Library()


@register.simple_tag
def documents_get_api_image_url(obj, **kwargs):
    return obj.get_api_image_url(**kwargs)
