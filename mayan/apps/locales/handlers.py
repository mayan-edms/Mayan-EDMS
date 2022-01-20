from django.apps import apps


def handler_user_locale_profile_create(sender, instance, created, **kwargs):
    UserLocaleProfile = apps.get_model(
        app_label='locales', model_name='UserLocaleProfile'
    )

    if created:
        UserLocaleProfile.objects.create(user=instance)
