from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import File
from django.http import StreamingHttpResponse
from django.views.decorators.cache import patch_cache_control

from .settings import (
    setting_image_cache_time, setting_image_generation_timeout
)
from .tasks import task_content_object_image_generate
from .utils import IndexedDictionary


class APIImageViewMixin:
    """
    get: Returns an image representation of the selected object.
    """
    def get_serializer(self, *args, **kwargs):
        return None

    def get_serializer_class(self):
        return None

    def get_content_type(self):
        return ContentType.objects.get_for_model(model=self.obj)

    def retrieve(self, request, **kwargs):
        self.set_object()
        query_dict = request.GET

        transformation_dictionary_list = IndexedDictionary(
            dictionary=query_dict
        ).as_dictionary_list()

        # An empty string is not a valid value for maximum_layer_order.
        # Fallback to None in case of a empty string.
        maximum_layer_order = request.GET.get('maximum_layer_order') or None
        if maximum_layer_order:
            maximum_layer_order = int(maximum_layer_order)

        task = task_content_object_image_generate.apply_async(
            kwargs={
                'content_type_id': self.get_content_type().pk,
                'object_id': self.obj.pk,
                'maximum_layer_order': maximum_layer_order,
                'transformation_dictionary_list': transformation_dictionary_list,
                'user_id': request.user.pk,
            }
        )

        kwargs = {'timeout': setting_image_generation_timeout.value}
        if settings.DEBUG:
            # In debug more, task are run synchronously, causing this method
            # to be called inside another task. Disable the check of nested
            # tasks when using debug mode.
            kwargs['disable_sync_subtasks'] = False

        cache_filename = task.get(**kwargs)

        cache_file = self.obj.cache_partition.get_file(filename=cache_filename)

        def file_generator():
            with cache_file.open() as file_object:
                while True:
                    chunk = file_object.read(File.DEFAULT_CHUNK_SIZE)
                    if not chunk:
                        break
                    else:
                        yield chunk

        response = StreamingHttpResponse(
            streaming_content=file_generator(), content_type='image'
        )

        if '_hash' in request.GET:
            patch_cache_control(
                response=response,
                max_age=setting_image_cache_time.value
            )
        return response

    def set_object(self):
        self.obj = self.get_object()
