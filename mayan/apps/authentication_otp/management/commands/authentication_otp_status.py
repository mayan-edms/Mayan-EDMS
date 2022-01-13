from django.core.management.base import BaseCommand

from ...models import UserOTPData


class Command(BaseCommand):
    help = 'Display the OTP status for a user.'
    missing_args_message = 'You must provide a username.'

    def add_arguments(self, parser):
        parser.add_argument(
            dest='username', help='Username for which OTP status will be displayed.',
            metavar='<username>'
        )

    def handle(self, username, **options):
        try:
            otp_data = UserOTPData.objects.get(user__username=username)
        except UserOTPData.DoesNotExist:
            status_text = 'Unknown username or OTP data is not initialized correctly.'
        else:
            if otp_data.is_enabled():
                status_text = 'OTP is enabled.'
            else:
                status_text = 'OTP is disabled.'

        self.stdout.write(msg='OTP state is: {}'.format(status_text))
