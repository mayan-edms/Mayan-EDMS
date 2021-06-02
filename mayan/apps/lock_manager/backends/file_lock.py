import hashlib
import logging
import json
import os
import threading
import time
import uuid

from django.conf import settings
from django.core.files import locks
from django.utils.encoding import force_bytes, force_text

from mayan.apps.storage.settings import setting_temporary_directory

from ..exceptions import LockError

from .base import LockingBackend

lock = threading.Lock()
logger = logging.getLogger(name=__name__)


class FileLock(LockingBackend):
    @classmethod
    def _acquire_lock(cls, name, timeout):
        instance = FileLock(name=name, timeout=timeout)
        return instance

    @classmethod
    def _initialize(cls):
        cls.lock_file = os.path.join(
            setting_temporary_directory.value, hashlib.sha256(
                force_bytes(s=settings.SECRET_KEY)
            ).hexdigest()
        )
        open(file=cls.lock_file, mode='a').close()
        logger.debug('lock_file: %s', cls.lock_file)

    @classmethod
    def _purge_locks(cls):
        lock.acquire()
        with open(file=cls.lock_file, mode='r+') as file_object:
            locks.lock(f=file_object, flags=locks.LOCK_EX)
            file_object.seek(0)
            file_object.truncate()
            lock.release()

    def _get_lock_dictionary(self):
        if self.timeout:
            result = {
                'expiration': time.time() + self.timeout,
                'uuid': self.uuid
            }
        else:
            result = {
                'expiration': 0,
                'uuid': self.uuid
            }

        return result

    def _init(self, name, timeout):
        self.name = name
        self.timeout = timeout
        self.uuid = force_text(s=uuid.uuid4())

        lock.acquire()
        with open(file=self.__class__.lock_file, mode='r+') as file_object:
            locks.lock(f=file_object, flags=locks.LOCK_EX)

            data = file_object.read()

            if data:
                file_locks = json.loads(s=data)
            else:
                file_locks = {}

            if name in file_locks:
                # Someone already got this lock, check to see if it is expired.
                if file_locks[name]['expiration'] and time.time() > file_locks[name]['expiration']:
                    # It expires and has expired, we re-acquired it.
                    file_locks[name] = self._get_lock_dictionary()
                else:
                    lock.release()
                    raise LockError
            else:
                file_locks[name] = self._get_lock_dictionary()

            file_object.seek(0)
            file_object.truncate()
            file_object.write(json.dumps(obj=file_locks))
            lock.release()

    def _release(self):
        lock.acquire()
        with open(file=self.__class__.lock_file, mode='r+') as file_object:
            locks.lock(f=file_object, flags=locks.LOCK_EX)
            try:
                file_locks = json.loads(s=file_object.read())
            except EOFError:
                file_locks = {}

            if self.name in file_locks:
                if file_locks[self.name]['uuid'] == self.uuid:
                    file_locks.pop(self.name)
                else:
                    # Lock expired and someone else acquired it
                    pass
            else:
                # Lock expired and someone else released it
                pass

            file_object.seek(0)
            file_object.truncate()
            file_object.write(json.dumps(obj=file_locks))
            lock.release()
