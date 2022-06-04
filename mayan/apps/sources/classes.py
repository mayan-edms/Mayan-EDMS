import collections
import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.class_mixins import AppsModuleLoaderMixin
from mayan.apps.databases.classes import ModelBaseBackend

logger = logging.getLogger(name=__name__)


class DocumentCreateWizardStep(AppsModuleLoaderMixin):
    _deregistry = {}
    _loader_module_name = 'wizard_steps'
    _registry = {}

    @classmethod
    def deregister(cls, step):
        cls._deregistry[step.name] = step

    @classmethod
    def deregister_all(cls):
        for step in cls.get_all():
            cls.deregister(step=step)

    @classmethod
    def done(cls, wizard):
        return {}

    @classmethod
    def get(cls, name):
        for step in cls.get_all():
            if name == step.name:
                return step

    @classmethod
    def get_all(cls):
        return sorted(
            (
                step for step in cls._registry.values() if step.name not in cls._deregistry
            ), key=lambda x: x.number
        )

    @classmethod
    def get_choices(cls, attribute_name):
        return [
            (step.name, getattr(step, attribute_name)) for step in cls.get_all()
        ]

    @classmethod
    def get_form_initial(cls, wizard):
        return {}

    @classmethod
    def get_form_kwargs(cls, wizard):
        return {}

    @classmethod
    def post_upload_process(cls, document, query_string=None):
        for step in cls.get_all():
            step.step_post_upload_process(
                document=document, query_string=query_string
            )

    @classmethod
    def register(cls, step):
        if step.name in cls._registry:
            raise Exception('A step with this name already exists: %s' % step.name)

        if step.number in [reigstered_step.number for reigstered_step in cls.get_all()]:
            raise Exception('A step with this number already exists: %s' % step.name)

        cls._registry[step.name] = step

    @classmethod
    def reregister(cls, name):
        cls._deregistry.pop(name)

    @classmethod
    def reregister_all(cls):
        cls._deregistry = {}

    @classmethod
    def step_post_upload_process(cls, document, query_string=None):
        """
        Optional method executed when the wizard ends to allow the step to
        perform its action.
        """


SourceBackendActionNamedTuple = collections.namedtuple(
    typename='SourceBackendAction', field_names=(
        'name', 'accept_files', 'arguments', 'confirmation', 'method'
    )
)


class SourceBackendAction(SourceBackendActionNamedTuple):
    def __new__(
        cls, name, accept_files=False, arguments=None, confirmation=True, method=None
    ):
        if not method:
            method = 'action_{}'.format(name)
        return super().__new__(
            cls, name=name, accept_files=accept_files,
            arguments=arguments or (), confirmation=confirmation,
            method=method
        )


class SourceBackend(ModelBaseBackend):
    """
    Base class for the source backends.

    The fields attribute is a list of dictionaries with the format:
    {
        'name': ''  # Field internal name
        'label': ''  # Label to show to users
        'initial': ''  # Field initial value
        'default': ''  # Default value.
    }
    """
    _backend_app_label = 'sources'
    _backend_model_name = 'Source'
    _loader_module_name = 'source_backends'

    @classmethod
    def post_load_modules(cls):
        for source_backend in cls.get_all():
            source_backend.intialize()

    @classmethod
    def get_action(cls, name):
        for action in cls.actions:
            if action.name == name:
                return action

        raise KeyError('Unknown source action `{}`.'.format(name))

    @classmethod
    def get_actions(cls):
        return getattr(cls, 'actions', ())

    @classmethod
    def get_fields(cls):
        return getattr(cls, 'fields', {})

    @classmethod
    def get_upload_form_class(cls):
        return getattr(cls, 'upload_form_class', None)

    @classmethod
    def get_setup_form_schema(cls):
        result = {
            'fields': cls.get_fields(),
            'widgets': cls.get_widgets(),
        }
        if hasattr(cls, 'field_order'):
            result['field_order'] = cls.field_order
        else:
            result['field_order'] = ()

        return result

    @classmethod
    def get_widgets(cls):
        return getattr(cls, 'widgets', {})

    @classmethod
    def intialize(cls):
        """
        Optional method for subclasses execute their own initialization
        code.
        """

    def clean(self):
        """
        Optional method to validate backend data before saving.
        """

    def create(self):
        """
        Called after the source model's .save() method for new
        instances.
        """

    def delete(self):
        """
        Called before the source model's .delete() method.
        """

    def execute_action(self, request, name, **kwargs):
        action = self.get_action(name=name)
        clean_kwargs = self.get_action_kwargs(action=action, **kwargs)
        clean_kwargs['request'] = request

        return getattr(self, action.method)(**clean_kwargs)

    def get_action_kwargs(self, action, **kwargs):
        clean_kwargs = {}
        for argument in action.arguments:
            clean_kwargs[argument] = kwargs.get(argument)

        if action.accept_files:
            clean_kwargs['file'] = kwargs.get('file')

        return clean_kwargs

    def get_action_context(self, name, view, **kwargs):
        action = self.get_action(name=name)
        clean_kwargs = self.get_action_kwargs(action=action, **kwargs)
        clean_kwargs['view'] = view

        try:
            return getattr(
                self, 'get_{}_context'.format(action.method)
            )(**clean_kwargs)
        except AttributeError:
            """Non fatal. The context method is optional."""

    def get_task_extra_kwargs(self):
        return {}

    def get_view_context(self, context, request):
        return {}

    def save(self):
        """
        Called after the source model's .save() method for existing
        instances.
        """


class SourceBackendNull(SourceBackend):
    label = _('Null backend')
