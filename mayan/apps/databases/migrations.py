import logging

from django.db import migrations

logger = logging.getLogger(name=__name__)


class RemoveIndexConditional(migrations.RemoveIndex):
    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        model = to_state.apps.get_model(app_label, self.model_name)
        if self.allow_migrate_model(schema_editor.connection.alias, model):
            to_model_state = to_state.models[app_label, self.model_name_lower]
            try:
                index = to_model_state.get_index_by_name(self.name)
            except ValueError:
                """Ignore as this is expected."""
            else:
                schema_editor.add_index(model, index)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        model = from_state.apps.get_model(app_label, self.model_name)

        if self.name in model._meta.indexes:
            if self.allow_migrate_model(schema_editor.connection.alias, model):
                from_model_state = from_state.models[app_label, self.model_name_lower]
                index = from_model_state.get_index_by_name(self.name)
                schema_editor.remove_index(model, index)

    def state_forwards(self, app_label, state):
        model_state = state.models[app_label, self.model_name_lower]
        indexes = model_state.options[self.option_name]

        if self.name in indexes:
            model_state.options[self.option_name] = [idx for idx in indexes if idx.name != self.name]
            state.reload_model(app_label, self.model_name_lower, delay=True)
