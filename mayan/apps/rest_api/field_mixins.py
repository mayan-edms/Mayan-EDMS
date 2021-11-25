from django.contrib.admin.utils import help_text_for_field, label_for_field
from django.core.exceptions import FieldDoesNotExist


class AutoHelpTextLabelFieldMixin:
    def bind(self, *args, **kwargs):
        result = super().bind(*args, **kwargs)

        try:
            model = self.root.Meta.model
        except AttributeError:
            return result
        else:
            try:
                field = model._meta.get_field(field_name=self.source)
            except FieldDoesNotExist:
                return result
            else:
                field_name = field.name

                if not self.label:
                    self.label = label_for_field(
                        model=model, name=field_name
                    )

                if not self.help_text:
                    self.help_text = help_text_for_field(
                        model=model, name=field_name
                    )

                return result
