from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoAdminSingleton',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True,
                        primary_key=True
                    )
                ),
                (
                    'password', models.CharField(
                        max_length=128, null=True, verbose_name='Password',
                        blank=True
                    )
                ),
                (
                    'password_hash', models.CharField(
                        max_length=128, null=True,
                        verbose_name='Password hash', blank=True
                    )
                ),
                (
                    'account', models.ForeignKey(
                        verbose_name='Account', blank=True,
                        to=settings.AUTH_USER_MODEL, null=True,
                        on_delete=models.CASCADE
                    )
                ),
            ],
            options={
                'verbose_name': 'Autoadmin properties',
                'verbose_name_plural': 'Autoadmin properties',
            },
            bases=(models.Model,),
        ),
    ]
