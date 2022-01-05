from django.core.management.base import BaseCommand

from ...models import UserOTPData


class Command(BaseCommand):
    help = 'Disable OTP for a user.'
    missing_args_message = 'You must provide a username.'

    def add_arguments(self, parser):
        parser.add_argument(
            dest='username', help='Username for which OTP will be disabled.',
            metavar='<username>'
        )

    def handle(self, username, **options):
        try:
            otp_data = UserOTPData.objects.get(user__username=username)
        except UserOTPData.DoesNotExist:
            result_text = 'Unknown username or OTP data is not initialized correctly.'
        else:
            if otp_data.is_enabled():
                otp_data.disable()

                if otp_data.is_enabled():
                    result_text = 'Unable to disable OTP.'
                else:
                    result_text = 'OTP disabled.'
            else:
                result_text = 'OTP is already disabled.'

        self.stdout.write(result_text)
