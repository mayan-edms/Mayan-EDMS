#!/bin/sh
if [ -n "$1" ]; then
	./manage.py runserver_plus $1 --adminmedia ./static/admin/
else
	./manage.py runserver_plus --adminmedia ./static/admin/
fi
