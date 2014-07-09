from __future__ import absolute_import

from django.conf.urls import url

from .cleanup import cleanup

cleanup_functions = [cleanup]
