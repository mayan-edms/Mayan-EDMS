from rest_framework.mixins import CreateModelMixin


class CreateOnlyFieldSerializerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_create_view():
            # Remove the create only fields if the view is anything other
            # than a create view.
            for field in getattr(self.Meta, 'create_only_fields', ()):
                # Use a default of None to avoid an error when trying to
                # remove a create only field already removed by the dynamic
                # fields mixin.
                self.fields.pop(field, None)

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
        fields_exclude = self.context.get('fields_exclude', '').split(',')
        fields_only = self.context.get('fields_only', '').split(',')

        self.fields_only = {None: ()}
        self.fields_only.update(
            self.group_fields(field_change_list=fields_only)
        )
        self.fields_exclude = {None: ()}
        self.fields_exclude.update(
            self.group_fields(field_change_list=fields_exclude)
        )

        self.update_fields(
            fields_exclude=self.fields_exclude[None],
            fields_only=self.fields_only[None]
        )

    def bind(self, field_name, parent):
        super().bind(field_name=field_name, parent=parent)

        self.update_fields(
            fields_exclude=getattr(
                self.root, 'fields_exclude', {}
            ).get(
                field_name, ()
            ),
            fields_only=getattr(
                self.root, 'fields_only', {}
            ).get(
                field_name, ()
            )
        )

    def group_fields(self, field_change_list, serializer_name=None):
        """
        Group all fields to be changed by object instance.
        Return a dictionary objects instance keys with their fields as
        sets.
        """
        serializers_fields = {}

        for field_change_name in field_change_list:
            if field_change_name:
                if '__' in field_change_name:
                    field_name, child_fields = field_change_name.split('__', 1)

                    related_serializer_fields = self.group_fields(
                        field_change_list=(child_fields,),
                        serializer_name=field_name
                    )

                    for key, value in related_serializer_fields.items():
                        serializers_fields.setdefault(key, set())
                        serializers_fields[key].update(value)
                else:
                    field_name = field_change_name

                serializers_fields.setdefault(serializer_name, set())
                serializers_fields[serializer_name].add(field_name)

        return serializers_fields

    def update_fields(self, fields_exclude=None, fields_only=None):
        fields_exclude = fields_exclude or ()
        fields_only = fields_only or ()

        if fields_only:
            for field_name in list(self.fields):
                if field_name not in fields_only:
                    self.fields.pop(field_name, None)

        for field_name in fields_exclude:
            if field_name not in self.fields_exclude:
                self.fields.pop(field_name, None)
