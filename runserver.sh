#!/bin/sh
if [ -n "$1" ]; then
        ./manage.py runserver $1
else
        ./manage.py runserver
fi
