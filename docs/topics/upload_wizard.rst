=============
Upload wizard
=============

The steps needed to upgrade a document using form-tools' ``SessionWizard``
were hardcoded in the ``source`` app. This made it very difficult to add or remove
wizard steps.

The steps of the wizard are now defined by a new class called
``sources.wizard.WizardStep``. The existing steps to select a document type,
enter metadata and tag the document, have been converted to function as
``WizardSteps`` subclasses. The converted steps now live in

``sources.wizards.WizardStepDocumentType``, ``tag.wizard_steps.WizardStepTags``,
and ``metadata.wizard_steps.WizardStepMetadata``.

The steps need to define the following methods:

- ``done``: This method is execute when the wizard finished the last step
  an enter the step where the actual file are uploaded. This steps is used
  to encode form data into the URL query string that will be passed to the
  document upload view for each file uploaded.

- ``condition``: This method is used to display the step conditionally.
  If this method return True it will be displayed during the upload wizard
  execution. To skip the step, return False or None.

- ``get_form_initial``: This method is used to return the initial data
  for the step form. Use this method to set up initial values for the step's
  form fields.

- ``step_post_upload_process``: This method will be executed once the
  document finishes uploading. Use this method to process the information
  encoded in the URL querystring by the step's `done`` method.

Once the ``WizardStep`` subclass is defined, it needs to be registered. This
is done by calling the ``.register`` method of the ``WizardStep`` class with
the subclass as the argument. Example::

    WizardStep.register(WizardStepMetadata)

This statement must be located after the subclass definition. Finally,
the module defining the wizard step must be imported so that it is loaded
with the rest of the code and enabled. The best place to do this is in the
``.ready`` method of the apps' ``apps.py`` module. Example::

    class TagsApp(MayanAppConfig):
        has_rest_api = True
        has_tests = True
        name = 'tags'
        verbose_name = _('Tags')

        def ready(self):
            super(TagsApp, self).ready()
            from actstream import registry

            from .wizard_steps import WizardStepTags  # NOQA

The ``WizardStep`` class also allows for unregistering existing steps. This
is accomplished by calling the ``.deregister`` method of the ``WizardStep``
class and passing the subclass as the argument. This method should
also be called inside the ``.ready`` method of an apps' ``apps.py``
module. Example::


    class TagsApp(MayanAppConfig):
        has_rest_api = True
        has_tests = True
        name = 'tags'
        verbose_name = _('Tags')

        def ready(self):
            super(TagsApp, self).ready()
            from actstream import registry

            from metadata.wizard_steps import WizardStepMetadata  # NOQA
            from sources.wizards import WizardStep  # NOQA
            from .wizard_steps import WizardStepTags  # NOQA

            WizardStep.deregister(WizardStepTags)


This will cause the tags assigment step to not be assigned to the upload
wizard anymore.
