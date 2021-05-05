import json
import logging

from django.db import models
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from .literals import IMPORT_ERROR_EXCLUSION_TEXTS

logger = logging.getLogger(name=__name__)


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


class ExtraDataModelMixin:
    def __init__(self, *args, **kwargs):
        _instance_extra_data = kwargs.pop('_instance_extra_data', {})
        result = super().__init__(*args, **kwargs)
        for key, value in _instance_extra_data.items():
            setattr(self, key, value)

        return result


class ValueChangeModelMixin:
    @classmethod
    def from_db(cls, db, field_names, values):
        new = super().from_db(db=db, field_names=field_names, values=values)
        new._values_previous = dict(zip(field_names, values))
        return new

    def __init__(self, *args, **kwargs):
        self._values_previous = kwargs
        super().__init__(*args, **kwargs)

    def _get_field_previous_value(self, field):
        return self._values_previous[field]

    def _has_field_changed(self, field):
        if self._state.adding:
            if getattr(self, field) != self._values_previous[field]:
                return True

        return False
