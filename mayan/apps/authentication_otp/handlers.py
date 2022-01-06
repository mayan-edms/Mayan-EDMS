from django.apps import apps


def handler_initialize_new_user_otp_data(sender, instance, **kwargs):
    UserOTPData = apps.get_model(
        app_label='authentication_otp', model_name='UserOTPData'
    )

    if kwargs['created']:
        UserOTPData.objects.create(user=instance)
