from django.contrib import contenttypes
from django.db import models
from django.utils.encoding import force_text

import mptt

from mayan.apps.acls.classes import ModelPermission

from .links import link_object_copy
from .menus import menu_object
from .permissions import permission_object_copy


class ModelCopy:
    _registry = {}
    _lazy = {}

    @staticmethod
    def method_instance_copy(self, values=None):
        model_copy = ModelCopy.get(model=self._meta.model)
        return model_copy.copy(instance=self, values=values)

    @classmethod
    def add_fields_lazy(cls, model, **kwargs):
        cls._lazy.setdefault(model, [])
        cls._lazy[model].append(kwargs)

    @classmethod
    def get(cls, model):
        return cls._registry[model]

    def __init__(
        self, model, acl_bind_link=True, condition=None, bind_link=False,
        excludes=None, register_permission=False, extra_kwargs=None
    ):
        self.condition = condition
        self.excludes = excludes or {}
        self.extra_kwargs = extra_kwargs or {}
        self.fields = []
        self.fields_copy = []
        self.fields_foreign_keys = []
        self.fields_generic_related = []
        self.fields_many_to_many = []
        self.fields_reverse_related = []
        self.fields_many_to_many_reverse_related = []
        self.fields_related_one_to_one = []
        self.fields_unique = []

        self.model = model
        self.__class__._registry[model] = self
        model.add_to_class(
            name='copy_instance', value=ModelCopy.method_instance_copy
        )
        if bind_link:
            menu_object.bind_links(
                links=(link_object_copy,), sources=(model,), position=99
            )

        if register_permission:
            ModelPermission.register(
                model=model, permissions=(permission_object_copy,),
                bind_link=acl_bind_link
            )

        for entry in self.__class__._lazy.get(model, ()):
            self.add_fields(**entry)
            self.__class__._lazy.get(model).pop()

    def __str__(self):
        return force_text(s=self.label)

    def _evaluate_field_get_for_field(self, field, instance, value, values):
        context = {'instance': instance}
        context.update(values)

        field_value_gets = self.field_value_gets.get(field, None)
        if field_value_gets:
            related_model = self.model._meta.get_field(field).related_model or self.model._meta.get_field(field).model
            final_filter = {}
            for key, value in field_value_gets.items():
                final_filter[key] = value.format(**context)

            value = related_model._meta.default_manager.get(**final_filter)

        field_value_templates = self.field_value_templates.get(field, None)
        if field_value_templates:
            value = field_value_templates.format(**context) or None

        return value

    def add_fields(
        self, field_names, field_value_gets=None, field_values=None,
        field_value_templates=None, unique_conditional=None
    ):
        self.unique_conditional = unique_conditional or {}
        self.field_value_gets = field_value_gets or {}
        self.field_value_templates = field_value_templates or {}
        self.field_values = field_values or {}

        for field_name in field_names:
            self.fields.append(field_name)

            field = self.model._meta.get_field(field_name=field_name)

            if isinstance(field, models.fields.reverse_related.OneToOneRel):
                self.fields_related_one_to_one.append(field_name)
            elif isinstance(field, models.fields.reverse_related.ManyToOneRel):
                self.fields_reverse_related.append(field_name)
            elif isinstance(field, models.fields.related.ForeignKey):
                self.fields_foreign_keys.append(field_name)
            elif isinstance(field, contenttypes.fields.GenericRelation):
                self.fields_generic_related.append(field_name)
            elif isinstance(field, contenttypes.fields.GenericForeignKey):
                self.fields_foreign_keys.append(field_name)
            elif isinstance(field, models.fields.related.ManyToManyField):
                self.fields_many_to_many.append(field_name)
            elif isinstance(field, models.fields.reverse_related.ManyToManyRel):
                self.fields_many_to_many_reverse_related.append(field.related_name)
            else:
                if field.unique:
                    self.fields_unique.append(field_name)
                else:
                    self.fields_copy.append(field_name)

    def copy(self, instance, values=None):
        values = values or {}

        if self.excludes:
            if self.model._meta.default_manager.filter(pk=instance.pk, **self.excludes).exists():
                return

        if isinstance(self.model, mptt.models.MPTTModelBase):
            node_map = {instance.pk: None}
            self.field_value_templates = {
                'parent_id': '{parent_id}'
            }

            for source_node in instance.get_descendants(include_self=True):
                if source_node.parent:
                    values['parent_id'] = node_map[source_node.parent.pk]
                else:
                    values['parent_id'] = ''

                new_node = self._copy(
                    instance=source_node, values=values,
                    _get_or_create=self.extra_kwargs.get('get_or_create', False)
                )
                if not values['parent_id']:
                    result = new_node
                node_map[source_node.pk] = new_node.pk

            return result
        else:
            return self._copy(instance=instance, values=values)

    def _copy(self, instance, values=None, _get_or_create=False):
        context = {'instance': instance}
        context.update(values)

        new_model_dictionary = {}

        # Static values.
        for field, value in self.field_values.items():
            new_model_dictionary[field] = value

        # Static values templates.
        for field, value in self.field_value_templates.items():
            result = value.format(**context) or None
            new_model_dictionary[field] = result

        # Base fields whose values are copied.
        for field in self.fields_copy:
            value = values.get(field, getattr(instance, field))

            value = self._evaluate_field_get_for_field(
                field=field, instance=instance, value=value, values=values
            )
            new_model_dictionary[field] = value

        # Base fields with unique values.
        for field in self.fields_unique:
            base_value = getattr(instance, field)
            counter = 1

            while True:
                value = '{}_{}'.format(base_value, counter)
                if not self.model._meta.default_manager.filter(**{field: value}).exists():
                    break

                counter = counter + 1

            value = self._evaluate_field_get_for_field(
                field=field, instance=instance, value=value, values=values
            )
            new_model_dictionary[field] = value

        # Foreign keys.
        for field in self.fields_foreign_keys:
            value = values.get(field, getattr(instance, field))

            value = self._evaluate_field_get_for_field(
                field=field, instance=instance, value=value, values=values
            )
            new_model_dictionary[field] = value

        # Fields that are given an unique value if a condition is met.
        for field in self.unique_conditional:
            if self.unique_conditional[field](
                instance=instance, new_instance_dictionary=new_model_dictionary
            ):
                base_value = getattr(instance, field)
                counter = 1

                while True:
                    value = '{}_{}'.format(base_value, counter)
                    if not self.model._meta.default_manager.filter(**{field: value}).exists():
                        break

                    counter = counter + 1

                value = self._evaluate_field_get_for_field(
                    field=field, instance=instance, value=value, values=values
                )
                new_model_dictionary[field] = value

        if _get_or_create:
            new_instance, created = self.model._meta.default_manager.get_or_create(
                **new_model_dictionary
            )
        else:
            new_instance = self.model(**new_model_dictionary)
            new_instance.save()

        # Many to many fields added after instance creation.
        for field in self.fields_many_to_many:
            getattr(new_instance, field).set(getattr(instance, field).all())

        # Many to many reverse related fields added after instance creation.
        for field in self.fields_many_to_many_reverse_related:
            getattr(new_instance, field).set(getattr(instance, field).all())

        # Reverse related.
        for field in self.fields_reverse_related:
            related_field = self.model._meta.get_field(field_name=field)
            related_field_name = related_field.field.name

            for related_instance in getattr(instance, field).all():
                values.update({related_field_name: new_instance})
                related_instance.copy_instance(
                    values=values
                )

        # Reverse related one to one.
        for field in self.fields_related_one_to_one:
            related_field = self.model._meta.get_field(field_name=field)
            related_field_name = related_field.field.name

            getattr(instance, field).copy_instance(
                values={related_field_name: new_instance}
            )

        # Generic relations.
        for field in self.fields_generic_related:
            related_field = self.model._meta.get_field(field_name=field)
            related_field_name = 'content_object'

            for related_instance in getattr(instance, field).all():
                related_instance.copy_instance(
                    values={related_field_name: new_instance}
                )

        return new_instance

    def get_fields_verbose_names(self):
        result = []

        for field_name in self.fields:
            field = self.model._meta.get_field(field_name=field_name)

            verbose_name = getattr(field, 'verbose_name', None)

            if not verbose_name and field.related_model:
                verbose_name = field.related_model._meta.verbose_name

            result.append(verbose_name)

        return result

    def test_condition(self, instance):
        if self.condition:
            return self.condition(instance=instance)
        else:
            return True


class MissingItem:
    _registry = []

    @classmethod
    def get_all(cls):
        return cls._registry

    @classmethod
    def get_missing(cls):
        result = []
        for item in cls.get_all():
            if item.condition():
                result.append(item)
        return result

    def __init__(self, label, condition, description, view):
        self.label = label
        self.condition = condition
        self.description = description
        self.view = view
        self.__class__._registry.append(self)


class PropertyHelper:
    """
    Makes adding fields using __class__.add_to_class easier.
    Each subclass must implement the `constructor` and the `get_result`
    method.
    """
    @staticmethod
    @property
    def constructor(source_object):
        return PropertyHelper(source_object)

    def __init__(self, instance):
        self.instance = instance

    def __getattr__(self, name):
        return self.get_result(name=name)

    def get_result(self, name):
        """
        The method that produces the actual result. Must be implemented
        by each subclass.
        """
        raise NotImplementedError
