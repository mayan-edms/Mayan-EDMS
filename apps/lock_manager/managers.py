try:
    from psycopg2 import OperationalError
except ImportError:
    class OperationalError(Exception):
        pass

import datetime

from django.db.utils import DatabaseError
from django.db.utils import IntegrityError
from django.db import transaction
from django.db import models

from lock_manager.exceptions import LockError


class LockManager(models.Manager):
    @transaction.commit_manually
    def acquire_lock(self, name, timeout=None):
        lock = self.model(name=name, timeout=timeout)
        try:
            lock.save(force_insert=True)
        except IntegrityError:
            transaction.rollback()
            # There is already an existing lock
            # Check it's expiration date and if expired, delete it and 
            # create it again
            lock = self.model.objects.get(name=name)
            transaction.rollback()

            if datetime.datetime.now() > lock.creation_datetime + datetime.timedelta(seconds=lock.timeout):
                self.release_lock(name)
                lock.timeout=timeout
                lock.save()
                transaction.commit()
            else:
                raise LockError('Unable to acquire lock')
        except DatabaseError:
            transaction.rollback()
            # Special case for ./manage.py syncdb
        except (OperationalError, ImproperlyConfigured):
            transaction.rollback()
            # Special for DjangoZoom, which executes collectstatic media
            # doing syncdb and creating the database tables
        else:
            transaction.commit()
        
    @transaction.commit_manually
    def release_lock(self, name):
        lock = self.model.objects.get(name=name)
        lock.delete()
        transaction.commit()
