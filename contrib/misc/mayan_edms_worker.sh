#!/bin/sh

DJANGO_SETTINGS_MODULE='mayan.settings.celery_redis' celery -A mayan worker -l DEBUG -Ofair -B
