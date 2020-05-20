import os

from django.apps import apps
from django.core.exceptions import AppRegistryNotReady
from django.utils.translation.trans_real import DjangoTranslation


def patchDjangoTranslation():
    """
    Patch Django to prioritize the app translations over its own.
    Fixes GitLab issue #734 for Django 1.11
    Needs to be updated for future Django version unless this is fixed
    upstream.
    """

    def _add_installed_apps_translations_new(self):
        """Merges translations from each installed app."""
        try:
            # Django apps
            app_configs = [
                app for app in apps.get_app_configs() if app.name.startswith('django.')
            ]

            # Non Django apps
            app_configs = [
                app for app in apps.get_app_configs() if not app.name.startswith('django.')
            ]
            app_configs = reversed(app_configs)
        except AppRegistryNotReady:
            raise AppRegistryNotReady(
                "The translation infrastructure cannot be initialized before the "
                "apps registry is ready. Check that you don't make non-lazy "
                "gettext calls at import time.")
        for app_config in app_configs:
            localedir = os.path.join(app_config.path, 'locale')
            if os.path.exists(localedir):
                translation = self._new_gnu_trans(localedir)
                self.merge(translation)

    DjangoTranslation._add_installed_apps_translations = _add_installed_apps_translations_new
