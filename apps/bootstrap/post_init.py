from __future__ import absolute_import

from time import gmtime, strftime

from navigation.api import register_links
from main import __version__

from .links import (link_bootstrap_setup_create, link_bootstrap_setup_execute,
    link_bootstrap_setup_list, link_bootstrap_setup_edit, link_bootstrap_setup_delete,
    link_bootstrap_setup_view, link_bootstrap_setup_dump)
from .models import BootstrapSetup
from .classes import FixtureMetadata
from .literals import (FIXTURE_METADATA_CREATED, FIXTURE_METADATA_EDITED,
    FIXTURE_METADATA_MAYAN_VERSION, FIXTURE_METADATA_FORMAT, FIXTURE_METADATA_NAME,
    FIXTURE_METADATA_DESCRIPTION, DATETIME_STRING_FORMAT)

register_links([BootstrapSetup], [link_bootstrap_setup_view, link_bootstrap_setup_edit, link_bootstrap_setup_delete, link_bootstrap_setup_execute])
register_links([BootstrapSetup], [link_bootstrap_setup_list, link_bootstrap_setup_create, link_bootstrap_setup_dump], menu_name='secondary_menu')
register_links(['bootstrap_setup_list', 'bootstrap_setup_create', 'bootstrap_setup_dump'], [link_bootstrap_setup_list, link_bootstrap_setup_create, link_bootstrap_setup_dump], menu_name='secondary_menu')

FixtureMetadata(FIXTURE_METADATA_CREATED, generate_function=lambda fixture_instance: strftime(fixture_instance.created.strftime(DATETIME_STRING_FORMAT)))
FixtureMetadata(FIXTURE_METADATA_EDITED, generate_function=lambda fixture_instance: strftime(DATETIME_STRING_FORMAT, gmtime()))
FixtureMetadata(FIXTURE_METADATA_MAYAN_VERSION, generate_function=lambda fixture_instance: __version__)
FixtureMetadata(FIXTURE_METADATA_FORMAT, generate_function=lambda fixture_instance: fixture_instance.type)
FixtureMetadata(FIXTURE_METADATA_NAME, generate_function=lambda fixture_instance: fixture_instance.name)
FixtureMetadata(FIXTURE_METADATA_DESCRIPTION, generate_function=lambda fixture_instance: fixture_instance.description)
