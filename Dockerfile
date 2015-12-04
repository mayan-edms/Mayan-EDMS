FROM ubuntu:15.04

MAINTAINER Roberto Rosario "roberto.rosario@mayan-edms.com"

# Install base Ubuntu libraries
RUN apt-get update && apt-get install -y netcat-openbsd python-dev python-pip gpgv nginx libpq-dev git-core libjpeg-dev libmagic1 libpng-dev libreoffice libtiff-dev gcc ghostscript gpgv tesseract-ocr unpaper poppler-utils && apt-get clean && rm -rf /var/lib/apt/lists/* && rm -f /var/cache/apt/archives/*.deb

ENV MAYAN_INSTALL_DIR=/usr/local/lib/python2.7/dist-packages/mayan

# Install Mayan EDMS, latest production release
RUN pip install mayan-edms==2.0.0

# Install Python clients for PostgreSQL, REDIS, and uWSGI
RUN pip install psycopg2 redis uwsgi

# Create Mayan EDMS basic settings/local.py file
RUN mayan-edms.py createsettings

# Install Mayan EDMS static media files
RUN mayan-edms.py collectstatic --noinput

ADD docker /docker

# Setup Mayan EDMS settings file overrides
RUN cat /docker/conf/mayan/settings.py >> $MAYAN_INSTALL_DIR/settings/local.py

# Setup NGINX
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /docker/conf/nginx/mayan-edms /etc/nginx/sites-enabled/mayan-edms

# Setup UWSGI
RUN mkdir /var/log/uwsgi

# Persistent Mayan EDMS files
VOLUME $MAYAN_INSTALL_DIR/media

ENTRYPOINT ["/docker/entrypoint.sh"]

EXPOSE 80
CMD ["/docker/bin/run.sh"]
