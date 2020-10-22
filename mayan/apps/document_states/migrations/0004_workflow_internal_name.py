from django.db import migrations, models
from django.utils.text import slugify

from mayan.apps.common.validators import validate_internal_name


def operation_generate_internal_name(apps, schema_editor):
    Workflow = apps.get_model(
        app_label='document_states', model_name='Workflow'
    )
    internal_names = []

    for workflow in Workflow.objects.using(alias=schema_editor.connection.alias).all():
        # Slugify and replace dashes (not allowed) by underscores
        workflow.internal_name = slugify(workflow.label).replace('-', '_')
        if workflow.internal_name in internal_names:
            # Add a suffix in case two conversions yield the same
            # result.
            workflow.internal_name = '{}_'.format(
                workflow.internal_name
            )

        internal_names.append(workflow.internal_name)
        workflow.save()


class Migration(migrations.Migration):
    dependencies = [
        ('document_states', '0003_auto_20170325_0447'),
    ]

    operations = [
        # Add the internal name field but make it non unique
        # https://docs.djangoproject.com/en/1.10/howto/
        # writing-migrations/#migrations-that-add-unique-fields
        migrations.AddField(
            model_name='workflow',
            name='internal_name',
            field=models.CharField(
                db_index=False, default=' ',
                help_text='This value will be used by other apps to reference '
                'this workflow. Can only contain letters, numbers, and '
                'underscores.', max_length=255, unique=False, validators=[
                    validate_internal_name
                ], verbose_name='Internal name'
            ),
        ),

        # Generate the slugs based on the labels
        migrations.RunPython(
            code=operation_generate_internal_name,
            reverse_code=migrations.RunPython.noop
        ),

        # Make the internal name field unique
        # Add the internal name field but make it non unique
        # https://docs.djangoproject.com/en/1.10/howto/
        # writing-migrations/#migrations-that-add-unique-fields
        migrations.AlterField(
            model_name='workflow',
            name='internal_name',
            field=models.CharField(
                db_index=True,
                help_text='This value will be used by other apps to reference '
                'this workflow. Can only contain letters, numbers, and '
                'underscores.', max_length=255, unique=True, validators=[
                    validate_internal_name
                ], verbose_name='Internal name'
            ),
        ),
    ]
