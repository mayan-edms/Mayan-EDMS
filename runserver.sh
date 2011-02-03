#!/bin/sh
if [ -n "$1" ]; then
        ./manage.py runserver $1 --adminmedia ./site_media/admin_media/
else
        ./manage.py runserver --adminmedia ./site_media/admin_media/
fi
