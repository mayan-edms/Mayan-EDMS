#!/usr/bin/env python

import os
import socket
import sys
import time

import yaml
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader
import psycopg2

PORT_RETRY_DELAY = 1


class ServiceCheck:
    _registry = []

    class ServiceError(Exception):
        """Base exception."""

    class ServiceConnectionError(ServiceError):
        """
        Raised when a service is not reachable. Holds the underlying
        exception as text.
        """

    class UnknownService(ServiceError):
        """
        Raised when the name does not match any known service.
        """
        def __init__(self, klass):
            self.klass = klass

        def __str__(self):
            return 'Unknown service `{}`'.format(self.klass)

    @staticmethod
    def yaml_load(*args, **kwargs):
        defaults = {'Loader': SafeLoader}
        defaults.update(kwargs)

        return yaml.load(*args, **defaults)

    @classmethod
    def all(cls):
        return cls._registry

    @classmethod
    def match(cls, text):
        for klass in cls.all():
            if klass._match(text=text):
                return klass

        raise ServiceCheck.UnknownService(klass=text)

    @classmethod
    def register(cls, klass=None):
        cls._registry.append(klass or cls)

    def __init__(self, *args, **kwargs):

        self.retry_delay = kwargs.pop('retry_delay', PORT_RETRY_DELAY)

        self.args = args
        self.kwargs = kwargs

        self._init()

    def _init(self):
        """To be overloaded by subclass."""

    def _match(text):
        """To be overloaded by subclass."""

    def check(self):
        attempt = 1

        while True:
            print('Connection attempt #{} to: {}; '.format(attempt, self), end='')

            try:
                self._check()
            except ServiceCheck.ServiceConnectionError as e:
                print(e)
                time.sleep(self.retry_delay)
                attempt += 1
            else:
                print('Connected.')
                break


class PortConnectionCheck(ServiceCheck):
    def __str__(self):
        return 'port {}:{}'.format(self.address, self.port)

    def _check(self):
        try:
            with socket.create_connection(address=(self.address, self.port)):
                """Use as context manager to ensure connection is closed."""
        except socket.error as exception:
            raise ServiceCheck.ServiceConnectionError(exception)

    def _init(self):
        self.address = self.kwargs['address']
        self.port = self.kwargs['text']

    def _match(text):
        try:
            int(text)
        except ValueError:
            return False
        else:
            return True


class PostgreSQLServiceCheck(ServiceCheck):
    def __str__(self):
        return 'PostgreSQL database'

    def _check(self):
        try:
            databases = os.environ['MAYAN_DATABASES']
        except KeyError:
            raise ServiceCheck.ServiceError('Missing databases parameters.')
        else:
            databases = ServiceCheck.yaml_load(stream=databases)
            for database_name, database_parameters in databases.items():
                if database_parameters['ENGINE'] == 'django.db.backends.postgresql':
                    database_name = database_parameters.get('NAME')
                    kwargs = {
                        'database': database_name,
                        'host': database_parameters.get('HOST'),
                        'password': database_parameters.get('PASSWORD'),
                        'post': database_parameters.get('PORT'),
                        'user': database_parameters.get('USER'),
                    }

                    try:
                        with psycopg2.connect(**kwargs) as connection:
                            cursor = connection.cursor()
                            cursor.execute('SELECT version()')
                            cursor.fetchone()
                            cursor.close()
                    except psycopg2.OperationalError as exception:
                        raise ServiceCheck.ServiceConnectionError(exception)

    def _match(text):
        return text == 'postgresql'


class ServiceCollection:
    def __init__(self):
        self.entries = []

        for entry in sys.argv[1:]:
            address, klass = entry.split(':')

            service = ServiceCheck.match(text=klass)
            self.entries.append(
                service(address=address, text=klass)
            )

    def check(self):
        for entry in self.entries:
            entry.check()


PortConnectionCheck.register()
PostgreSQLServiceCheck.register()


if __name__ == '__main__':
    ServiceCollection().check()
