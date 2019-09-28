# vim:set ft=dockerfile:

####
# BASE_IMAGE - Bare bones image with the base packages needed to run Mayan EDMS
####

FROM debian:9.8-slim as BASE_IMAGE

LABEL maintainer="Roberto Rosario roberto.rosario@mayan-edms.com"

ENV PYTHONUNBUFFERED=1 \
    LC_ALL=C.UTF-8 \
    PROJECT_INSTALL_DIR=/opt/mayan-edms

# Debian package caching
ARG APT_PROXY
RUN set -x \
&& if [ "${APT_PROXY}" ]; \
    then echo "Acquire::http { Proxy \"http://${APT_PROXY}\"; };" > /etc/apt/apt.conf.d/01proxy \
; fi \
# Install base OS packages to run Mayan EDMS
&& DEBIAN_FRONTEND=noninteractive \
apt-get update \
&& apt-get install -y --no-install-recommends \
    exiftool \
    fonts-arphic-uming \
    fonts-arphic-ukai \
    ghostscript \
    gpgv \
    gnupg1 \
    graphviz \
    libfuse2 \
    libmagic1 \
    libmariadbclient18 \
    libreoffice \
    libpq5 \
    poppler-utils \
    redis-server \
    sane-utils \
    sudo \
    supervisor \
    tesseract-ocr \
# Remove make and build dependencies
&& apt-get remove make libproxy-tools libreoffice-avmedia-backend-vlc libvlc-bin libvlc5 libvlccore9 adwaita-icon-theme gsettings-desktop-schemas libgstreamer-plugins-base1.0-0 -y \
&& apt-get autoremove -y --purge \
# Add mayan user
&& adduser mayan --disabled-password --disabled-login --no-create-home --gecos "" \
# Pillow can't find zlib or libjpeg on aarch64 (ODROID C2)
&& if [ "$(uname -m)" = "aarch64" ]; then \
    ln -s /usr/lib/aarch64-linux-gnu/libz.so /usr/lib/ \
    && ln -s /usr/lib/aarch64-linux-gnu/libjpeg.so /usr/lib/ \
; fi \
# Pillow can't find zlib or libjpeg on armv7l (ODROID HC1)
&& if [ "$(uname -m)" = "armv7l" ]; then \
    ln -s /usr/lib/arm-linux-gnueabihf/libz.so /usr/lib/ \
    && ln -s /usr/lib/arm-linux-gnueabihf/libjpeg.so /usr/lib/ \
; fi \
# Discard data when Redis runs out of memory
&& echo "maxmemory-policy allkeys-lru" >> /etc/redis/redis.conf \
# Disable saving the Redis database
echo "save \"\"" >> /etc/redis/redis.conf \
# Only provision 1 database
&& echo "databases 1" >> /etc/redis/redis.conf

####
# BUILDER_IMAGE - This image buildS the Python package and is discarded afterwards
####

# Reuse image
FROM BASE_IMAGE as BUILDER_IMAGE

WORKDIR /src

# Copy the source files needed to build the Python package
COPY --chown=mayan:mayan requirements /src/requirements
COPY --chown=mayan:mayan \
    HISTORY.rst \
    LICENSE \
    MANIFEST.in \
    README.md \
    README.rst \
    setup.py \
    /src/

COPY --chown=mayan:mayan mayan /src/mayan

# Install development packages needed to build the Python packages
RUN DEBIAN_FRONTEND=noninteractive \
apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    libffi-dev \
    libjpeg-dev \
    libpng-dev \
    libpq-dev \
    libtiff-dev \
    zlib1g-dev \
    libssl-dev \
    g++ \
    gcc \
    python-dev \
    python-virtualenv \
&& mkdir -p "${PROJECT_INSTALL_DIR}" \
&& chown -R mayan:mayan "${PROJECT_INSTALL_DIR}" \
&& chown -R mayan:mayan /src

USER mayan
RUN python -m virtualenv "${PROJECT_INSTALL_DIR}" \
&& . "${PROJECT_INSTALL_DIR}/bin/activate" \
&& pip install --no-cache-dir --no-use-pep517 \
    librabbitmq==1.6.1 \
    mysql-python==1.2.5 \
    psycopg2==2.7.3.2 \
    redis==2.10.6 \
# psutil is needed by ARM builds otherwise gevent and gunicorn fail to start
&& UNAME=`uname -m` && if [ "${UNAME#*arm}" != $UNAME ]; then \
    pip install --no-cache-dir --no-use-pep517 \
    psutil==5.6.2 \
; fi \
# Install the Python packages needed to build Mayan EDMS
&& pip install --no-cache-dir --no-use-pep517 -r /src/requirements/build.txt \
# Build Mayan EDMS
&& python setup.py sdist \
# Install the built Mayan EDMS package
&& pip install --no-cache-dir --no-use-pep517 dist/mayan* \
# Install the static content
&& mayan-edms.py installjavascript \
&& MAYAN_STATIC_ROOT=${PROJECT_INSTALL_DIR}/static mayan-edms.py preparestatic --link --noinput

COPY --chown=mayan:mayan requirements/testing-base.txt "${PROJECT_INSTALL_DIR}"

####
# Final image - BASE_IMAGE + Mayan install directory from the builder image
####

FROM BASE_IMAGE

COPY --from=BUILDER_IMAGE --chown=mayan:mayan "${PROJECT_INSTALL_DIR}/" "${PROJECT_INSTALL_DIR}/"

USER root

COPY docker/rootfs /

VOLUME ["/var/lib/mayan"]

ENTRYPOINT ["entrypoint.sh"]

EXPOSE 8000
CMD ["mayan"]

RUN ${PROJECT_INSTALL_DIR}/bin/mayan-edms.py platformtemplate supervisord_docker > /etc/supervisor/conf.d/mayan.conf \
&& apt-get clean autoclean \
&& apt-get autoremove --purge -y \
&& rm -rf /var/lib/apt/lists/* \
&& rm -f /var/cache/apt/archives/*.deb \
# Remove temporary files owned by root from the platformtemplate step
&& rm /tmp/* \
# Keep displaying log messages to stdout
&& find /var/log -type f | while read f; do echo -ne '' > $f; done;
