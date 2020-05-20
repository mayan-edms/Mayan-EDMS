from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0005_auto_20170731_0452'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectEventSubscription',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                ('object_id', models.PositiveIntegerField()),
                (
                    'content_type', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='contenttypes.ContentType'
                    )
                ),
                (
                    'stored_event_type', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='object_subscriptions',
                        to='events.StoredEventType', verbose_name='Event type'
                    )
                ),
                (
                    'user', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='object_subscriptions',
                        to=settings.AUTH_USER_MODEL, verbose_name='User'
                    )
                ),
            ],
            options={
                'verbose_name': 'Object event subscription',
                'verbose_name_plural': 'Object event subscriptions',
            },
        ),
    ]
