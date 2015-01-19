from .api import GPG
from .settings import GPG_HOME, GPG_PATH, KEYSERVERS

gpg = GPG(binary_path=GPG_PATH, home=GPG_HOME, keyservers=KEYSERVERS)
