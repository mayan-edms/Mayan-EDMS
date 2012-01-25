from django_gpg.api import GPG
from django_gpg.conf.settings import KEYSERVERS, GPG_HOME

gpg = GPG(home=GPG_HOME, keyservers=KEYSERVERS)
