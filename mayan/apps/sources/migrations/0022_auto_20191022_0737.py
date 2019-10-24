from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sources', '0021_auto_20190629_0648'),
    ]

    operations = [
        migrations.AddField(
            model_name='imapemail',
            name='execute_expunge',
            field=models.BooleanField(
                default=True, help_text='Execute the IMAP expunge command '
                'after processing each email message.',
                verbose_name='Execute expunge'
            ),
        ),
        migrations.AddField(
            model_name='imapemail',
            name='mailbox_destination',
            field=models.CharField(
                blank=True, help_text='IMAP Mailbox to which processed '
                'messages will be copied.', max_length=96, null=True,
                verbose_name='Destination mailbox'
            ),
        ),
        migrations.AddField(
            model_name='imapemail',
            name='store_commands',
            field=models.TextField(
                blank=True, default='+FLAGS (\\Deleted)',
                help_text='IMAP STORE command to execute on messages '
                'after they are processed. One command per line. Use '
                'the commands specified in '
                'https://tools.ietf.org/html/rfc2060.html#section-6.4.6 or '
                'the custom commands for your IMAP server.', null=True,
                verbose_name='Store commands'
            ),
        ),
        migrations.AddField(
            model_name='imapemail',
            name='search_criteria',
            field=models.TextField(
                blank=True, default='NOT DELETED', help_text='Criteria to '
                'use when searching for messages to process. Use the '
                'format specified in '
                'https://tools.ietf.org/html/rfc2060.html#section-6.4.4',
                null=True, verbose_name='Search criteria'
            ),
        ),
    ]
