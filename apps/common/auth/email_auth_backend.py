# From: http://www.micahcarrick.com/django-email-authentication.html
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


class EmailAuthBackend(ModelBackend):
    """
    Email Authentication Backend

    Allows a user to sign in using an email/password pair rather than
    a username/password pair.
    """

    def authenticate(self, email=None, password=None):
        """
        Authenticate a user based on email address as the user name.
        """
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
