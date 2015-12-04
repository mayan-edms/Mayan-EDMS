from .api import GPG
from .settings import setting_gpg_home, setting_gpg_path, setting_keyservers

gpg = GPG(
    binary_path=setting_gpg_path.value, home=setting_gpg_home.value,
    keyservers=setting_keyservers.value
)
