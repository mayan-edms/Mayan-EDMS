# vim:set ft=dockerfile:

####################
# Base image start #
####################

FROM debian:9.4-slim as BASE_IMAGE

MAINTAINER Roberto Rosario "roberto.rosario@mayan-edms.com"

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1
ENV LC_ALL C.UTF-8
ENV PROJECT_INSTALL_DIR=/opt/mayan-edms
ENV PYTHON_PIP=${PROJECT_INSTALL_DIR}/bin/pip

ARG APT_PROXY
# Package caching
RUN if [ "${APT_PROXY}" ]; then echo "Acquire::http { Proxy \"http://${APT_PROXY}\"; };" > /etc/apt/apt.conf.d/01proxy; fi

# Install base Ubuntu libraries
RUN apt-get update && \
apt-get install -y --no-install-recommends \
        g++ \
        gcc \
        ghostscript \
        gpgv \
        gnupg1 \
        graphviz \
        libffi-dev \
        libfuse2 \
        libjpeg-dev \
        libmagic1 \
        default-libmysqlclient-dev \
        libpng-dev \
        libpq-dev \
        libreoffice \
        libtiff-dev \
        poppler-utils \
        python-dev \
        python-setuptools \
        python-virtualenv \
        python-wheel \
        redis-server \
        sane-utils \
        sudo \
        supervisor \
        tesseract-ocr \
        zlib1g-dev \
        libssl-dev \
&& \
apt-get clean autoclean && \
apt-get autoremove --purge -y && \
rm -rf /var/lib/apt/lists/* && \
rm -f /var/cache/apt/archives/*.deb

# Install apt-get-install
ADD https://raw.githubusercontent.com/guilhem/apt-get-install/master/apt-get-install /usr/bin/
RUN chmod +x /usr/bin/apt-get-install

RUN adduser mayan --disabled-password --disabled-login --no-create-home --gecos ""

# Pillow can't find zlib or libjpeg on aarch64 (ODROID C2)
RUN if [ "$(uname -m)" = "aarch64" ]; then \
ln -s /usr/lib/aarch64-linux-gnu/libz.so /usr/lib/ && \
ln -s /usr/lib/aarch64-linux-gnu/libjpeg.so /usr/lib/ \
; fi

# Pillow can't find zlib or libjpeg on armv7l (ODROID HC1)
RUN if [ "$(uname -m)" = "armv7l" ]; then \
ln -s /usr/lib/arm-linux-gnueabihf/libz.so /usr/lib/ && \
ln -s /usr/lib/arm-linux-gnueabihf/libjpeg.so /usr/lib/ \
; fi

# Discard data when Redis runs out of memory
RUN echo "maxmemory-policy allkeys-lru" >> /etc/redis/redis.conf

# Disable saving the Redis database
RUN echo "save \"\"" >> /etc/redis/redis.conf

# Only provision 1 database
RUN echo "databases 1" >> /etc/redis/redis.conf

#####################
# Build image start #
#####################

FROM debian:9.4-slim as BUILDER_IMAGE

ARG APT_PROXY
# Package caching
RUN if [ "${APT_PROXY}" ]; then echo "Acquire::http { Proxy \"http://${APT_PROXY}\"; };" > /etc/apt/apt.conf.d/01proxy; fi

WORKDIR /code

COPY . /code

RUN apt-get update && apt-get install make python-dev python-pip -y

RUN pip install -r requirements/build.txt

ENV LC_ALL C.UTF-8

RUN touch docker/Makefile

RUN make wheel

RUN chmod 777 dist -R

#####################
# Final image start #
#####################

FROM BASE_IMAGE

RUN mkdir -p /opt

RUN python /usr/lib/python2.7/dist-packages/virtualenv.py $PROJECT_INSTALL_DIR

WORKDIR $PROJECT_INSTALL_DIR

COPY --from=BUILDER_IMAGE /code/dist/*.whl .

COPY --from=BUILDER_IMAGE /code/contrib/scripts/docker/run-tests.sh .

COPY --from=BUILDER_IMAGE /code/requirements/testing-base.txt requirements-testing.txt

COPY --from=BUILDER_IMAGE /code/docker/version .

# Fix ownership
RUN chown -R mayan:mayan $PROJECT_INSTALL_DIR

# Install build Mayan EDMS
RUN sudo -u mayan $PYTHON_PIP install --no-cache-dir --no-use-pep517 *.whl && \
rm *.whl

# Install Python clients for librabbitmq, MySQL, PostgreSQL, REDIS
RUN sudo -u mayan $PYTHON_PIP install --no-cache-dir --no-use-pep517 librabbitmq==1.6.1 mysql-python==1.2.5 psycopg2==2.7.3.2 redis==2.10.6

# Setup supervisor
COPY docker/etc/supervisor/mayan.conf /etc/supervisor/conf.d

RUN mkdir /var/lib/mayan
VOLUME ["/var/lib/mayan"]

COPY docker/entrypoint.sh /usr/local/bin/
RUN ln -s usr/local/bin/entrypoint.sh / # backwards compat
ENTRYPOINT ["entrypoint.sh"]

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
