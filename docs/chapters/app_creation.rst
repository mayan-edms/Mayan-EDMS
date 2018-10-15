************
App creation
************

Mayan EDMS apps are essentially Django app with some extra code to register
navigation, permissions and other relationships.


App modules
===========

- __init__.py

  Should be empty if possible. No initialization code should be here, use the
  ready() method of the MayanAppConfig class in the apps.py module.

- admin.py

  Standard Django app module to define how models are to be presented in the
  admin interface.

- api_views.py

  REST API views go here. Mayan EDMS uses Django REST Framework API view
  classes.

- apps.py

  Contains the MayanAppConfig subclass as required by Django 1.7 and up. This
  is a place to define the app name and translatable verbose name as well as
  code to be execute when the modules of the app are ready.

- classes.py

  Hold python classes to be used internally or externally. Any class defined by
  the app that is not a model.

- events.py

  Define event class instances that are later committed to a log by custom
  code.

- exceptions.py

  Custom exceptions defined by the app.

- fields.py

  Place any custom form field classed you define here.

- forms.py

  Standard Django app module that hold custom form classes.

- handlers.py

  Contains the signal handlers, functions that will process a given signal
  emitted from this or other apps. Connect the handler functions to the
  corresponding signal in the ready() method of the MayanAppConfig subclass in
  apps.py

- links.py

  Defines the links to be used by the app. Import only from the navigation app
  and the local permissions.py file.

- literals.py

  Stores magic numbers, module choices (if static), settings defaults, and
  constants. Should contain all capital case variables. Must not import from
  any other module.

- managers.py

  Standard Django app module that hold custom model managers. These act as
  model class method to performs actions in a series of model instances or
  utilitarian actions on external models instances.

- models.py

  Standard Django app module that defines ORM persistent data schema.

- permissions.py

  Defines the permissions to be used to validate user access by links and views.
  Imports only from the permissions app. Link or view conditions such as
  testing for is_staff or is_super_user flag are defined in this same module.

- runtime.py

  Use this module when you need the same instance of a class for the entire app.
  This module acts as a shared memory space for the other modules of the app or
  other apps.

- serializers.py

  Hold Django REST Framework serializers used by the api_views.py module.

- settings.py

  Define the configuration settings instances that the app will use.

- signals.py

  Any custom defined signal goes here.

- statistics.py

  Provides functions that will compute any sort of statistical information on
  the app’s data.

- tasks.py

  Code to be execute in the background or as an out-of-process action.

- tests/ directory

  Hold test modules. There should be one test_*.py module for each aspect being
  tested, examples: test_api.py, test_views.py, test_parsers.py, test_permissions.py
  Any shared constant data used by the tests should be added to tests/literals.py

- utils.py

  Holds utilitarian code that doesn't fit on any other app module or that is
  used by several modules in the app. Anything used internally by the app that
  is not a class or a literal (should be as little as possible)

- widgets.py

  HTML widgets go here. This should be the only place with presentation
  directives in the app (aside the templates).


Views
=====

The module common.generics provides custom generic class based views to be used.
The basic views used to create, edit, view and delete objects in Mayan EDMS
are: SingleObjectCreateView, SingleObjectDetailView, SingleObjectEditView,
and SingleObjectListView

These views handle aspects relating to view permissions, object permissions,
post action redirection and template context generation.
