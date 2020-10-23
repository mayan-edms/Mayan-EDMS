from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'label', models.CharField(
                        db_index=True, help_text='A short text describing '
                        'the theme.', max_length=128, unique=True,
                        verbose_name='Label'
                    )
                ),
                (
                    'stylesheet', models.TextField(
                        blank=True, help_text='The CSS stylesheet to '
                        'change the appearance of the different user '
                        'interface elements.', verbose_name='Stylesheet'
                    )
                ),
            ],
            options={
                'verbose_name': 'Theme',
                'verbose_name_plural': 'Themes',
                'ordering': ('label',),
            },
        ),
        migrations.CreateModel(
            name='UserThemeSetting',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'theme', models.ForeignKey(
                        blank=True, null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='user_setting', to='appearance.Theme',
                        verbose_name='Theme'
                    )
                ),
                (
                    'user', models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='theme_settings',
                        to=settings.AUTH_USER_MODEL, verbose_name='User'
                    )
                ),
            ],
            options={
                'verbose_name': 'User theme setting',
                'verbose_name_plural': 'User theme settings',
            },
        ),
    ]
