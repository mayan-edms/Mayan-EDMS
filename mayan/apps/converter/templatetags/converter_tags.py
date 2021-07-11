from django.template import Library
from django.urls import reverse

from ..classes import AppImageErrorImage
from ..exceptions import AppImageError

register = Library()


@register.simple_tag
def converter_get_object_image_data(obj, transformation_instance_list):
    try:
        return {
            'url': obj.get_api_image_url(
                transformation_instance_list=transformation_instance_list
            )
        }
    except AppImageError as exception:
        app_image_error_image = AppImageErrorImage.get(
            name=exception.error_name
        )

        return {
            'app_image_error_image': app_image_error_image,
            'url': reverse(
                viewname='rest_api:app-image-error-image', kwargs={
                    'app_image_error_name': exception.error_name
                }
            )
        }
