# vim:set ft=dockerfile:

####################
# Base image start #
####################

FROM ubuntu:16.04 as BASE_IMAGE

MAINTAINER Roberto Rosario "roberto.rosario@mayan-edms.com"

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1
ENV LANG en_US.UTF-8
ENV PROJECT_INSTALL_DIR=/usr/local/lib/python2.7/dist-packages/mayan

ARG APT_PROXY
# Package caching
RUN if [ "${APT_PROXY}" ]; then echo "Acquire::http { Proxy \"http://${APT_PROXY}\"; };" > /etc/apt/apt.conf.d/01proxy; fi

# Install base Ubuntu libraries
RUN apt-get update && \
apt-get install -y --no-install-recommends \
        curl \
        g++ \
        gcc \
        gettext-base \
        ghostscript \
        gpgv \
        graphviz \
        libffi-dev \
        libjpeg-dev \
        libmagic1 \
        libmysqlclient-dev \
        libpng-dev \
        libpq-dev \
        libreoffice \
        libtiff-dev \
        locales \
        netcat-openbsd \
        poppler-utils \
        python-dev \
        python-pip \
        python-setuptools \
        python-wheel \
        redis-server \
        supervisor \
        tesseract-ocr \
        zlib1g-dev \
&& \
apt-get clean autoclean && \
apt-get autoremove --purge -y && \
rm -rf /var/lib/apt/lists/* && \
rm -f /var/cache/apt/archives/*.deb

# Switch to UTF locale
RUN echo "LC_ALL=\"en_US.UTF-8\"" >> /etc/default/locale && \
locale-gen en_US.UTF-8 && \
update-locale LANG=en_US.UTF-8 && \
export LC_ALL=en_US.UTF-8

# Install apt-get-install
ADD https://raw.githubusercontent.com/guilhem/apt-get-install/master/apt-get-install /usr/bin/
RUN chmod +x /usr/bin/apt-get-install

# Install Python clients for PostgreSQL, REDIS, librabbitmq
RUN pip install psycopg2==2.7.3.2 redis==2.10.6 mysql-python==1.2.5 librabbitmq==1.6.1

RUN adduser mayan --disabled-password --disabled-login --no-create-home --gecos ""

# Pillow can't find zlib or libjpeg on aarch64
RUN if [ "$(uname -m)" = "aarch64" ]; then \
ln -s /usr/lib/aarch64-linux-gnu/libz.so /usr/lib/ && \
ln -s /usr/lib/aarch64-linux-gnu/libjpeg.so /usr/lib/ \
; fi

#####################
# Build image start #
#####################

FROM python:2-alpine3.7 as BUILDER_IMAGE

WORKDIR /code

COPY . /code

RUN apk update && \
    apk add make

RUN pip install -r requirements/build.txt

RUN make wheel

RUN chmod 777 dist -R

#####################
# Final image start #
#####################

FROM BASE_IMAGE

WORKDIR /root/

COPY --from=BUILDER_IMAGE /code/dist/*.whl .

# Install build Mayan EDMS
RUN pip install *.whl && \
rm *.whl

# Setup supervisor
#RUN mkdir /etc/supervisor.d/
COPY docker/etc/supervisor/beat.conf /etc/supervisor/conf.d
COPY docker/etc/supervisor/gunicorn.conf /etc/supervisor/conf.d
COPY docker/etc/supervisor/redis.conf /etc/supervisor/conf.d
COPY docker/etc/supervisor/workers.conf /etc/supervisor/conf.d

# Create the directory for the logs
RUN mkdir /var/log/mayan

# Fix ownership
RUN chown -R mayan:mayan $PROJECT_INSTALL_DIR

# Allow flanker to autogenerate its PLY files
RUN chown -R mayan:mayan /usr/local/lib/python2.7/dist-packages/flanker/

RUN mkdir /var/lib/mayan
VOLUME ["/var/lib/mayan"]

COPY docker/entrypoint.sh /usr/local/bin/
RUN ln -s usr/local/bin/entrypoint.sh / # backwards compat
ENTRYPOINT ["entrypoint.sh"]

# Healthcheck setup
HEALTHCHECK --interval=15s --timeout=1s --retries=20 \
  CMD curl -s -f http://localhost/authentication/login/ | grep 'form' > /dev/null || exit 1

EXPOSE 8000
CMD ["mayan"]

RUN rm /root/.cache -R
RUN rm -rf /tmp/*

RUN apt-get -y autoremove --purge && apt-get -y autoclean && apt-get -y clean

RUN rm -rf /usr/share/man/*
RUN rm -rf /usr/share/doc/*

RUN find /var/lib/apt -type f | xargs rm -f
RUN find /var/cache -type f -exec rm -rf {} \;

RUN find /var/log -type f | while read f; do echo -ne '' > $f; done;
