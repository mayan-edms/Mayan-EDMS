#!/bin/sh

DJANGO_SETTINGS_MODULE='mayan.settings.celery_redis' celery -A mayan worker -l DEBUG -Q checkouts,mailing,uploads,converter,ocr,tools,indexing,metadata -Ofair -B
