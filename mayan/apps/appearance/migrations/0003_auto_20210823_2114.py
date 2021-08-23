import bleach

from django.db import migrations


def code_sanitize_themes(apps, schema_editor):
    """
    Sanitize all theme stylesheets.
    """
    Theme = apps.get_model(
        app_label='appearance', model_name='Theme'
    )

    for theme in Theme.objects.all():
        theme.stylesheet = bleach.clean(
            text=theme.stylesheet, tags=('style',)
        )
        theme.save()


class Migration(migrations.Migration):
    dependencies = [
        ('appearance', '0002_add_theme_for_existing_users'),
    ]

    operations = [
        migrations.RunPython(
            code=code_sanitize_themes,
            reverse_code=migrations.RunPython.noop
        )
    ]
