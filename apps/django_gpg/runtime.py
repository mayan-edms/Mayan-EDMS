from django_gpg.api import GPG
from django_gpg.conf.settings import KEYSERVERS

gpg = GPG(keyservers=KEYSERVERS)
