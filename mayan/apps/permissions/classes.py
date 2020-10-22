from importlib import import_module
import itertools
import logging

from django.apps import apps
from django.core.exceptions import PermissionDenied
from django.db.utils import OperationalError, ProgrammingError
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .exceptions import InvalidNamespace

logger = logging.getLogger(name=__name__)


@python_2_unicode_compatible
class PermissionNamespace(object):
    _registry = {}

    @classmethod
    def all(cls):
        return cls._registry.values()

    @classmethod
    def get(cls, name):
        try:
            return cls._registry[name]
        except KeyError:
            raise InvalidNamespace(
                'Invalid namespace name. This is probably an obsolete '
                'permission namespace, execute the management command '
                '"purgepermissions" and try again.'
            )

    def __init__(self, name, label):
        self.name = name
        self.label = label
        self.permissions = []
        self.__class__._registry[name] = self

    def __str__(self):
        return force_text(s=self.label)

    def add_permission(self, name, label):
        permission = Permission(namespace=self, name=name, label=label)
        self.permissions.append(permission)
        return permission


@python_2_unicode_compatible
class Permission(object):
    _imported_app = []
    _permissions = {}
    _stored_permissions_cache = {}

    @classmethod
    def all(cls, as_choices=False):
        if as_choices:
            results = []

            for namespace, permissions in itertools.groupby(cls.all(), lambda entry: entry.namespace):
                permission_options = [
                    (force_text(s=permission.pk), permission) for permission in permissions
                ]
                results.append(
                    (namespace, permission_options)
                )

            return results
        else:
            # Return sorted permissions by namespace.name
            return sorted(
                cls._permissions.values(), key=lambda x: x.namespace.name
            )

    @classmethod
    def check_user_permissions(cls, permissions, user):
        for permission in permissions:
            if permission.stored_permission.user_has_this(user=user):
                return True

        logger.debug(
            'User "%s" does not have permissions "%s"', user, permissions
        )
        raise PermissionDenied(_('Insufficient permissions.'))

    @classmethod
    def get(cls, pk, class_only=False):
        if class_only:
            return cls._permissions[pk]
        else:
            return cls._permissions[pk].stored_permission

    @classmethod
    def initialize(cls):
        module_name = 'permissions'

        for app in apps.get_app_configs():
            # Keep track of the apps that have already been imported to
            # avoid importing them more than once. Does not causes a problem,
            # it is an optimization to speed up statups.
            if app not in cls._imported_app:
                try:
                    import_module('{}.{}'.format(app.name, module_name))
                except ImportError as exception:
                    non_fatal_messages = (
                        'No module named {}'.format(module_name),
                        'No module named \'{}.{}\''.format(app.name, module_name)
                    )

                    if force_text(s=exception) not in non_fatal_messages:
                        logger.error(
                            'Error importing %s %s.py file; %s', app.name,
                            module_name, exception
                        )
                        raise
                finally:
                    cls._imported_app.append(app)

        # Invalidate cache always. This is for tests that build a new memory
        # only database and cause all cache references built in the .ready()
        # method to be invalid.
        cls.invalidate_cache()

        for permission in cls.all():
            permission.stored_permission

    @classmethod
    def invalidate_cache(cls):
        cls._stored_permissions_cache = {}

    def __init__(self, namespace, name, label):
        self.namespace = namespace
        self.name = name
        self.label = label
        self.pk = self.get_pk()
        self.__class__._permissions[self.pk] = self

    def __repr__(self):
        return self.pk

    def __str__(self):
        return force_text(s=self.label)

    def get_pk(self):
        return '%s.%s' % (self.namespace.name, self.name)

    @property
    def stored_permission(self):
        try:
            return self.__class__._stored_permissions_cache[self.pk]
        except KeyError:
            StoredPermission = apps.get_model(
                app_label='permissions', model_name='StoredPermission'
            )

            try:
                stored_permission, created = StoredPermission.objects.get_or_create(
                    namespace=self.namespace.name,
                    name=self.name,
                )

                self.__class__._stored_permissions_cache[self.pk] = stored_permission
                return stored_permission
            except (OperationalError, ProgrammingError):
                """
                This error is expected when trying to initialize the
                stored permissions during the initial creation of the
                database. Can be safely ignore under that situation.
                """
