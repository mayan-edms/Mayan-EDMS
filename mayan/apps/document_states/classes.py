from importlib import import_module
import logging

from django.apps import apps
from django.db.utils import OperationalError, ProgrammingError
from django.utils import six
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.classes import PropertyHelper
from mayan.apps.templating.classes import Template

from .exceptions import WorkflowStateActionError

__all__ = ('WorkflowAction',)
logger = logging.getLogger(name=__name__)


class DocumentStateHelper(PropertyHelper):
    @staticmethod
    @property
    def constructor(*args, **kwargs):
        return DocumentStateHelper(*args, **kwargs)

    def get_result(self, name):
        return self.instance.workflows.get(workflow__internal_name=name)


class WorkflowActionMetaclass(type):
    _registry = {}

    def __new__(mcs, name, bases, attrs):
        new_class = super(WorkflowActionMetaclass, mcs).__new__(
            mcs, name, bases, attrs
        )

        if not new_class.__module__ == __name__:
            mcs._registry[
                '{}.{}'.format(new_class.__module__, name)
            ] = new_class

        return new_class


class WorkflowActionBase(object):
    fields = ()


class WorkflowAction(
    six.with_metaclass(WorkflowActionMetaclass, WorkflowActionBase)
):
    previous_dotted_paths = ()

    @staticmethod
    def initialize():
        for app in apps.get_app_configs():
            try:
                import_module('{}.workflow_actions'.format(app.name))
            except ImportError as exception:
                if force_text(exception) not in ('No module named workflow_actions', 'No module named \'{}.workflow_actions\''.format(app.name)):
                    logger.error(
                        'Error importing %s workflow_actions.py file; %s',
                        app.name, exception
                    )

        for action_class in WorkflowAction.get_all():
            action_class.migrate()

    @classmethod
    def clean(cls, request, form_data=None):
        return form_data

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_all(cls):
        return sorted(cls._registry.values(), key=lambda x: x.label)

    @classmethod
    def id(cls):
        return '{}.{}'.format(cls.__module__, cls.__name__)

    @classmethod
    def migrate(cls):
        WorkflowStateAction = apps.get_model(
            app_label='document_states', model_name='WorkflowStateAction'
        )
        for previous_dotted_path in cls.previous_dotted_paths:
            try:
                WorkflowStateAction.objects.filter(
                    action_path=previous_dotted_path
                ).update(action_path=cls.id())
            except (OperationalError, ProgrammingError):
                # Ignore errors during the database migration and
                # quit further attempts.
                return

    def __init__(self, form_data=None):
        self.form_data = form_data

    def get_form_schema(self, request=None):
        result = {
            'fields': self.fields or {},
            'media': getattr(self, 'media', {}),
            'widgets': getattr(self, 'widgets', {}),
        }

        if hasattr(self, 'field_order'):
            result['field_order'] = self.field_order

        return result

    def render_field(self, field_name, context):
        try:
            result = Template(
                template_string=self.form_data.get(field_name, '')
            ).render(
                context=context
            )
        except Exception as exception:
            raise WorkflowStateActionError(
                _('%(field_name)s template error: %(exception)s') % {
                    'field_name': field_name, 'exception': exception
                }
            )

        logger.debug('%s template result: %s', field_name, result)

        return result
