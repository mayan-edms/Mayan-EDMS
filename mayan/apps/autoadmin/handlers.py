from django.apps import apps


def handler_auto_admin_account_password_change(sender, instance, **kwargs):
    AutoAdminSingleton = apps.get_model(
        app_label='autoadmin', model_name='AutoAdminSingleton'
    )

    auto_admin_properties, created = AutoAdminSingleton.objects.get_or_create()

    if instance == auto_admin_properties.account and \
       instance.password != auto_admin_properties.password_hash:
        # Only delete the auto admin properties when the password
        # has been changed
        auto_admin_properties.account = None
        auto_admin_properties.password = None
        auto_admin_properties.password_hash = None
        auto_admin_properties.save()
