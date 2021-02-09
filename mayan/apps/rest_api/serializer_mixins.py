from rest_framework.mixins import CreateModelMixin


class CreateOnlyFieldSerializerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_create_view():
            # Remove the create only fields if the view is anything other
            # than a create view.
            for field in getattr(self.Meta, 'create_only_fields', ()):
                self.fields.pop(field)

    def is_create_view(self):
        request = self.context.get('request')
        view = self.context.get('view')

        if request and view:
            if isinstance(view, CreateModelMixin) and request.method.lower() == 'post':
                # This is a create view with a request to create an instance.
                return True

        return False
