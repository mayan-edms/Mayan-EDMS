from django.db import models
from django.contrib.auth.models import User, Group

from actstream import registry

registry.register(User)
registry.register(Group)
