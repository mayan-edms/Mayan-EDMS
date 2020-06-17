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
                    [
                        dirpath, [
                            os.path.join(dirpath, filename) for filename in filenames
                        ]
                    ]
                )

    return packages

install_requires = """
django==2.2.13
Pillow==7.1.2
PyPDF2==1.26.0
PyYAML==5.3.1
Whoosh==2.7.4
celery==4.4.5
django-activity-stream==0.8.0
django-celery-beat==2.0.0
django-colorful==1.3
django-cors-headers==3.2.1
django-formtools==2.2
django-mathfilters==1.0.0
django-model-utils==4.0.0
django-mptt==0.11.0
django-pure-pagination==0.3.0
django-qsstats-magic==1.1.0
django-solo==1.1.3
django-stronghold==0.4.0
django-widget-tweaks==1.4.8
djangorestframework==3.11.0
djangorestframework-recursive==0.1.2
drf-yasg==1.17.1
extract-msg==0.23.3
flanker==0.9.11
flex==6.14.1
furl==2.1.0
fusepy==3.0.1
gevent==20.4.0
graphviz==0.14
gunicorn==20.0.4
mock==4.0.2
node-semver==0.8.0
packaging==20.3
pycountry==19.8.18
pycryptodome==3.9.7
pyocr==0.7.2
python-dateutil==2.8.1
python-magic==0.4.15
python_gnupg==0.4.6
pytz==2020.1
requests==2.23.0
sh==1.13.1
swagger-spec-validator==2.5.0
whitenoise==5.0.1
""".split()

with open(file='README.rst') as file_object:
    readme = file_object.read()

with open(file='HISTORY.rst') as file_object:
    history = file_object.read()

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
