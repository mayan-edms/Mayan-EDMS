from __future__ import unicode_literals

import logging
import json
import threading
import time
import uuid

from django.core.files import locks

from common.utils import mkstemp

from ..exceptions import LockError

lock = threading.Lock()
logger = logging.getLogger(__name__)

temporary_file = mkstemp()[1]
logger.debug('temporary_file: %s', temporary_file)


class FileLock(object):
    @classmethod
    def acquire_lock(cls, name, timeout=None):
        instance = FileLock(name=name, timeout=timeout)
        return instance

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

    def __init__(self, name, timeout):
        self.name = name
        self.timeout = timeout or 0
        self.uuid = uuid.uuid4().get_hex()

        lock.acquire()
        with open(temporary_file, 'r+') as file_object:
            locks.lock(f=file_object, flags=locks.LOCK_EX)

            data = file_object.read()

            if data:
                file_locks = json.loads(data)
            else:
                file_locks = {}

            if name in file_locks:
                # Someone already got this lock, check to see if it is expired
                if file_locks[name]['expiration'] and time.time() > file_locks[name]['expiration']:
                    # It expires and has expired, we re-acquired it
                    file_locks[name] = self._get_lock_dictionary()
                else:
                    lock.release()
                    raise LockError
            else:
                file_locks[name] = self._get_lock_dictionary()

            file_object.seek(0)
            file_object.truncate()
            file_object.write(json.dumps(file_locks))
            lock.release()

    def release(self):
        lock.acquire()
        with open(temporary_file, 'r+') as file_object:
            locks.lock(f=file_object, flags=locks.LOCK_EX)
            try:
                file_locks = json.loads(file_object.read())
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
            file_object.write(json.dumps(file_locks))
            lock.release()
