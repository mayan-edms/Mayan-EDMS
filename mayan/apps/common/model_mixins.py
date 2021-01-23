import json
import logging

from django.db import models
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(name=__name__)
IMPORT_ERROR_EXCLUSION_TEXTS = (
    'doesn\'t look like a module path', 'No module named'
)


class BackendModelMixin(models.Model):
    _backend_model_null_backend = None

    backend_path = models.CharField(
        max_length=128, help_text=_(
            'The dotted Python path to the backend class.'
        ), verbose_name=_('Backend path')
    )
    backend_data = models.TextField(
        blank=True, help_text=_(
            'JSON encoded data for the backend class.'
        ), verbose_name=_('Backend data')
    )

    class Meta:
        abstract = True

    def get_backend(self):
        """
        Retrieves the backend by importing the module and the class.
        """
        try:
            return import_string(dotted_path=self.backend_path)
        except ModuleNotFoundError as exception:
            logger.error(
                'ModuleNotFoundError while importing backend: %s; %s',
                self.backend_path, exception
            )
            if self._backend_model_null_backend:
                return self._backend_model_null_backend
            else:
                raise
        except ImportError as exception:
            logger.error(
                'ImportError while importing backend: %s; %s',
                self.backend_path, exception
            )
            for import_error_exclusion_text in IMPORT_ERROR_EXCLUSION_TEXTS:
                if import_error_exclusion_text in str(exception):
                    raise

            if self._backend_model_null_backend:
                return self._backend_model_null_backend
            else:
                raise

    def get_backend_instance(self):
        return self.get_backend()(
            model_instance_id=self.id, **self.get_backend_data()
        )

    def get_backend_label(self):
        """
        Return the label that the backend itself provides. The backend is
        loaded but not initialized. As such the label returned is a class
        property.
        """
        return self.get_backend().label

    get_backend_label.short_description = _('Backend')
    get_backend_label.help_text = _('The backend class for this entry.')

    def get_backend_data(self):
        return json.loads(s=self.backend_data or '{}')

    def set_backend_data(self, obj):
        self.backend_data = json.dumps(obj=obj)
