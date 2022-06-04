from rest_framework.mixins import CreateModelMixin

from .literals import DEFAULT_DYNAMIC_FIELD_SEPARATOR


class CreateOnlyFieldSerializerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_create_view():
            # Remove the create only fields if the view is anything other
            # than a create view.
            self._excluded_fields.update(
                getattr(self.Meta, 'create_only_fields', ())
            )

    def is_create_view(self):
        request = self.context.get('request')
        view = self.context.get('view')

        if request and view:
            if isinstance(view, CreateModelMixin) and request.method.lower() == 'post':
                # This is a create view with a request to create an instance.
                return True

        return False


class DynamicFieldListSerializerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._excluded_fields = set()

        # Handle top level fields.
        fields_exclude = self.context.get('fields_exclude', '').split(',')
        fields_only = self.context.get('fields_only', '').split(',')
        matched_exclude = []
        matched_only = []

        for field_exclude in fields_exclude:
            parts = field_exclude.split(DEFAULT_DYNAMIC_FIELD_SEPARATOR)
            matched_exclude.append(parts[-1])

        for field_only in fields_only:
            parts = field_only.split(DEFAULT_DYNAMIC_FIELD_SEPARATOR)
            if parts[0]:
                matched_only.append(parts[0])

        self.update_excluded_fields(
            fields_exclude=matched_exclude, fields_only=matched_only
        )

    def bind(self, field_name, parent):
        super().bind(field_name=field_name, parent=parent)

        # Handle fields from included serializers.

        # Context retrieval is repeated to ensure context is available after
        # __init__.
        fields_exclude = self.context.get('fields_exclude', '').split(',')
        fields_only = self.context.get('fields_only', '').split(',')
        matched_exclude = []
        matched_only = []
        path = self.get_path()
        path_level = len(path)

        for field_exclude in fields_exclude:
            parts = field_exclude.split(DEFAULT_DYNAMIC_FIELD_SEPARATOR)
            if path == parts[0:path_level]:
                local_field_name = parts[-1]
                matched_exclude.append(local_field_name)

        for field_only in fields_only:
            parts = field_only.split(DEFAULT_DYNAMIC_FIELD_SEPARATOR)
            if path == parts[0:path_level]:
                try:
                    local_field_name = parts[path_level]
                except IndexError:
                    pass
                else:
                    matched_only.append(local_field_name)

        self.update_excluded_fields(
            fields_exclude=matched_exclude, fields_only=matched_only
        )

    def get_fields(self):
        fields = super().get_fields()

        # Copy keys to avoid modifying them in the loop.
        field_names = list(fields.keys())

        for field in field_names:
            if field in self._excluded_fields:
                fields.pop(field)

        return fields

    def get_path(self):
        result = [self.field_name]

        parent = self.parent
        while True:
            if parent:
                if parent.field_name:
                    result.append(parent.field_name)

                parent = parent.parent
            else:
                break

        result.reverse()

        return result

    def update_excluded_fields(self, fields_exclude=None, fields_only=None):
        fields_exclude = set(fields_exclude or ())
        fields_only = set(fields_only or ())

        self._excluded_fields.update(fields_exclude)

        if fields_only:
            serializer_fields = set(super().get_fields())

            self._excluded_fields.update(
                serializer_fields - fields_only
            )
