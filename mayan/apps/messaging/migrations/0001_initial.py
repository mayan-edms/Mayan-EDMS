from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('subject', models.CharField(help_text='Short description of this message.', max_length=255, verbose_name='Subject')),
                ('body', models.TextField(help_text='The actual content of the message.', verbose_name='Body')),
                ('read', models.BooleanField(default=False, help_text='This field determines if the message has been read or not.', verbose_name='Read')),
                ('date_time', models.DateTimeField(auto_now_add=True, help_text='Date and time of the message creation.', verbose_name='Creation date and time')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='messaging.Message', verbose_name='Parent message')),
                ('sender_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'ordering': ('-date_time',),
            },
        ),
    ]
