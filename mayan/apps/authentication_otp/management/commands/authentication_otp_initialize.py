from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ...models import UserOTPData


class Command(BaseCommand):
    help = 'Initialize the OTP state data for all users.'

    def handle(self, *args, **options):
        count = 0

        for user in get_user_model().objects.all():
            user_data, created = UserOTPData.objects.get_or_create(user=user)
            if created:
                count += 1

        self.stdout.write(msg='Completed for {} users.'.format(count))
