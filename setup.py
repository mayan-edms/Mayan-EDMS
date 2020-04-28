#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import mayan

PACKAGE_NAME = 'mayan-edms'
PACKAGE_DIR = 'mayan'

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


def find_packages(directory):
    # Compile the list of packages available, because distutils doesn't have
    # an easy way to do this.
    packages, data_files = [], []
    root_dir = os.path.dirname(__file__)
    if root_dir != '':
        os.chdir(root_dir)

    for dirpath, dirnames, filenames in os.walk(directory):
        if not dirpath.startswith('mayan/media'):
            # Ignore dirnames that start with '.'
            if os.path.basename(dirpath).startswith('.'):
                continue
            if '__init__.py' in filenames:
                packages.append('.'.join(fullsplit(dirpath)))
            elif filenames:
                data_files.append(
                    [dirpath, [os.path.join(dirpath, f) for f in filenames]]
                )

    return packages

install_requires = """
django==2.2.12
Pillow==7.0.0
PyPDF2==1.26.0
PyYAML==5.3.1
celery==4.3.0
django-activity-stream==0.8.0
django-celery-beat==1.5.0
django-colorful==1.3
django-cors-headers==2.5.2
django-formtools==2.2
django-mathfilters==1.0.0
django-model-utils==4.0.0
django-mptt==0.11.0
django-pure-pagination==0.3.0
django-qsstats-magic==1.1.0
django-solo==1.1.3
django-stronghold==0.4.0
django-widget-tweaks==1.4.8
djangorestframework==3.7.7
djangorestframework-recursive==0.1.2
drf-yasg==1.6.0
extract-msg==0.23.3
flanker==0.9.11
flex==6.14.0
furl==2.1.0
fusepy==3.0.1
gevent==1.4.0
graphviz==0.13.2
gunicorn==20.0.4
kombu==4.6.7
mock==4.0.2
node-semver==0.8.0
pycountry==19.8.18
pycryptodome==3.9.7
pyocr==0.6
python-dateutil==2.8.1
python-magic==0.4.15
python_gnupg==0.4.5
pytz==2019.1
requests==2.23.0
sh==1.12.14
swagger-spec-validator==2.4.3
whitenoise==5.0.1
""".split()

with open('README.rst') as f:
    readme = f.read()

with open('HISTORY.rst') as f:
    history = f.read()

setup(
    author='Roberto Rosario',
    author_email='roberto.rosario@mayan-edms.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Communications :: File Sharing',
    ],
    description=mayan.__description__,
    include_package_data=True,
    install_requires=install_requires,
    license='Apache 2.0',
    long_description=readme + '\n\n' + history,
    name=PACKAGE_NAME,
    packages=find_packages(PACKAGE_DIR),
    platforms=['any'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    scripts=['mayan/bin/mayan-edms.py'],
    url='https://gitlab.com/mayan-edms/mayan-edms',
    version=mayan.__version__,
    zip_safe=False,
)
