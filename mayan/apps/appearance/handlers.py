from django.apps import apps


def handler_user_theme_setting_create(sender, instance, created, **kwargs):
    UserThemeSetting = apps.get_model(
        app_label='appearance', model_name='UserThemeSetting'
    )

    if created:
        UserThemeSetting.objects.create(user=instance)
