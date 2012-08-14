from __future__ import absolute_import

from django.db import DatabaseError, transaction

from .models import App
from .links import app_registry_tool_link


@transaction.commit_on_success
def register_app(name, label, icon=None):
    try:
        app, created = App.objects.get_or_create(name=name)
    except DatabaseError:
        transaction.rollback()
        return None
    else:
        app.label = label
        if icon:
            app.icon = icon
        app.save()
        return app
