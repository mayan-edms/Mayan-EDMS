from django.db import migrations

from ..compatibility import RGBColorField

COLOR_BLUE = 'blu'
COLOR_CORAL = 'crl'
COLOR_CYAN = 'cya'
COLOR_GREENYELLOW = 'gry'
COLOR_KHAKI = 'kki'
COLOR_LIGHTGREY = 'lig'
COLOR_MAGENTA = 'mag'
COLOR_ORANGE = 'org'
COLOR_RED = 'red'
COLOR_YELLOW = 'yel'

RGB_VALUES = {
    COLOR_BLUE: '#0000ff',
    COLOR_CORAL: '#ff7f50',
    COLOR_CYAN: '#00ffff',
    COLOR_GREENYELLOW: '#adff2f',
    COLOR_KHAKI: '#f0e68c',
    COLOR_LIGHTGREY: '#d3d3d3',
    COLOR_MAGENTA: '#ff00ff',
    COLOR_ORANGE: '#ffa500',
    COLOR_RED: '#ff0000',
    COLOR_YELLOW: '#ffff00',
}


def code_convert_color_names_to_rgb(apps, schema_editor):
    Tag = apps.get_model(app_label='tags', model_name='Tag')

    for tag in Tag.objects.using(alias=schema_editor.connection.alias).all():
        tag.selection = RGB_VALUES[tag.color]
        tag.save()


class Migration(migrations.Migration):
    dependencies = [
        ('tags', '0001_initial')
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='selection',
            field=RGBColorField(default='#FFFFFF'),
            preserve_default=False,
        ),
        migrations.RunPython(code=code_convert_color_names_to_rgb)
    ]
