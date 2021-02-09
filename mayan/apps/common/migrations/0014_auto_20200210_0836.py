from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('common', '0013_auto_20190725_0452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlocaleprofile',
            name='language',
            field=models.CharField(
                choices=[
                    ('ar', 'Arabic'), ('bg', 'Bulgarian'),
                    ('bs', 'Bosnian'), ('cs', 'Czech'), ('da', 'Danish'),
                    ('de', 'German'), ('el', 'Greek'), ('en', 'English'),
                    ('es', 'Spanish'), ('fa', 'Persian'), ('fr', 'French'),
                    ('hu', 'Hungarian'), ('id', 'Indonesian'),
                    ('it', 'Italian'), ('lv', 'Latvian'),
                    ('nl', 'Dutch'), ('pl', 'Polish'),
                    ('pt', 'Portuguese'), ('pt-br', 'Portuguese (Brazil)'),
                    ('ro', 'Romanian'), ('ru', 'Russian'),
                    ('sl', 'Slovenian'), ('tr', 'Turkish'),
                    ('vi', 'Vietnamese'), ('zh-hans', 'Chinese (Simplified)')
                ], max_length=8, verbose_name='Language'
            ),
        ),
    ]
