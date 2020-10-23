from django.db import migrations, models
import django.db.models.deletion

import mayan.apps.common.validators


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('converter', '0013_auto_20180823_2353'),
    ]

    operations = [
        migrations.CreateModel(
            name='LayerTransformation',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'order', models.PositiveIntegerField(
                        blank=True, db_index=True, default=0,
                        help_text='Order in which the transformations will '
                        'be executed. If left unchanged, an automatic order '
                        'value will be assigned.', verbose_name='Order'
                    )
                ),
                (
                    'name', models.CharField(
                        choices=[
                            ('crop', 'Crop: left, top, right, bottom'),
                            ('draw_rectangle', 'Draw rectangle: left, top, right, bottom, fillcolor, outlinecolor, outlinewidth'),
                            ('draw_rectangle_percent', 'Draw rectangle (percents coordinates): left, top, right, bottom, fillcolor, outlinecolor, outlinewidth'),
                            ('flip', 'Flip'),
                            ('gaussianblur', 'Gaussian blur: radius'),
                            ('lineart', 'Line art'), ('mirror', 'Mirror'),
                            ('redaction_percent', 'Redaction: left, top, right, bottom'),
                            ('resize', 'Resize: width, height'),
                            ('rotate', 'Rotate: degrees, fillcolor'),
                            ('rotate180', 'Rotate 180 degrees'),
                            ('rotate270', 'Rotate 270 degrees'),
                            ('rotate90', 'Rotate 90 degrees'),
                            ('unsharpmask', 'Unsharp masking: radius, percent, threshold'),
                            ('zoom', 'Zoom: percent')
                        ], max_length=128, verbose_name='Name'
                    )
                ),
                (
                    'arguments', models.TextField(
                        blank=True, help_text='Enter the arguments for '
                        'the transformation as a YAML dictionary. '
                        'ie: {"degrees": 180}', validators=[
                            mayan.apps.common.validators.YAMLValidator()
                        ], verbose_name='Arguments'
                    )
                ),
                (
                    'enabled', models.BooleanField(
                        default=True, verbose_name='Enabled'
                    )
                ),
            ],
            options={
                'ordering': ('object_layer__stored_layer__order', 'order'),
                'verbose_name': 'Layer transformation',
                'verbose_name_plural': 'Layer transformations',
            },
        ),
        migrations.CreateModel(
            name='ObjectLayer',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True,
                        serialize=False, verbose_name='ID'
                    )
                ),
                ('object_id', models.PositiveIntegerField()),
                (
                    'enabled', models.BooleanField(
                        default=True, verbose_name='Enabled'
                    )
                ),
                (
                    'content_type', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='contenttypes.ContentType'
                    )
                ),
            ],
            options={
                'ordering': ('stored_layer__order',),
                'verbose_name': 'Object layer',
                'verbose_name_plural': 'Object layers',
            },
        ),
        migrations.CreateModel(
            name='StoredLayer',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True,
                        serialize=False, verbose_name='ID'
                    )
                ),
                (
                    'name', models.CharField(
                        max_length=64, unique=True, verbose_name='Name'
                    )
                ),
                (
                    'order', models.PositiveIntegerField(
                        db_index=True, unique=True, verbose_name='Order'
                    )
                ),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Stored layer',
                'verbose_name_plural': 'Stored layers',
            },
        ),
        migrations.AlterField(
            model_name='transformation',
            name='name',
            field=models.CharField(
                choices=[
                    ('crop', 'Crop: left, top, right, bottom'),
                    ('draw_rectangle', 'Draw rectangle: left, top, right, bottom, fillcolor, outlinecolor, outlinewidth'),
                    ('draw_rectangle_percent', 'Draw rectangle (percents coordinates): left, top, right, bottom, fillcolor, outlinecolor, outlinewidth'),
                    ('flip', 'Flip'),
                    ('gaussianblur', 'Gaussian blur: radius'),
                    ('lineart', 'Line art'), ('mirror', 'Mirror'),
                    ('redaction_percent', 'Redaction: left, top, right, bottom'),
                    ('resize', 'Resize: width, height'),
                    ('rotate', 'Rotate: degrees, fillcolor'),
                    ('rotate180', 'Rotate 180 degrees'),
                    ('rotate270', 'Rotate 270 degrees'),
                    ('rotate90', 'Rotate 90 degrees'),
                    ('unsharpmask', 'Unsharp masking: radius, percent, threshold'),
                    ('zoom', 'Zoom: percent')
                ], max_length=128, verbose_name='Name'
            ),
        ),
        migrations.AddField(
            model_name='objectlayer',
            name='stored_layer',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='object_layers', to='converter.StoredLayer',
                verbose_name='Stored layer'
            ),
        ),
        migrations.AddField(
            model_name='layertransformation',
            name='object_layer',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='transformations', to='converter.ObjectLayer',
                verbose_name='Object layer'
            ),
        ),
        migrations.AlterUniqueTogether(
            name='objectlayer',
            unique_together=set(
                [('content_type', 'object_id', 'stored_layer')]
            ),
        ),
        migrations.AlterUniqueTogether(
            name='layertransformation',
            unique_together=set([('object_layer', 'order')]),
        ),
    ]
