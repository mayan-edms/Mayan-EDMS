from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Workflow',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True,
                        primary_key=True
                    )
                ),
                (
                    'label', models.CharField(
                        unique=True, max_length=255, verbose_name='Label'
                    )
                ),
                (
                    'document_types', models.ManyToManyField(
                        related_name='workflows',
                        verbose_name='Document types',
                        to='documents.DocumentType'
                    )
                ),
            ],
            options={
                'verbose_name': 'Workflow',
                'verbose_name_plural': 'Workflows',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkflowInstance',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True,
                        primary_key=True
                    )
                ),
                (
                    'document', models.ForeignKey(
                        on_delete=models.CASCADE, related_name='workflows',
                        to='documents.Document', verbose_name='Document'
                    )
                ),
                (
                    'workflow', models.ForeignKey(
                        on_delete=models.CASCADE, related_name='instances',
                        to='document_states.Workflow',
                        verbose_name='Workflow'
                    )
                ),
            ],
            options={
                'verbose_name': 'Workflow instance',
                'verbose_name_plural': 'Workflow instances',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkflowInstanceLogEntry',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True,
                        primary_key=True
                    )
                ),
                (
                    'datetime', models.DateTimeField(
                        auto_now_add=True, verbose_name='Datetime',
                        db_index=True
                    )
                ),
                (
                    'comment', models.TextField(
                        verbose_name='Comment', blank=True
                    )
                ),
            ],
            options={
                'verbose_name': 'Workflow instance log entry',
                'verbose_name_plural': 'Workflow instance log entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkflowState',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True,
                        primary_key=True
                    )
                ),
                (
                    'label', models.CharField(
                        max_length=255, verbose_name='Label'
                    )
                ),
                (
                    'initial', models.BooleanField(
                        default=False, help_text='Select if this will be the '
                        'state with which you want the workflow to start in. '
                        'Only one state can be the initial state.',
                        verbose_name='Initial'
                    )
                ),
                (
                    'workflow', models.ForeignKey(
                        on_delete=models.CASCADE, related_name='states',
                        to='document_states.Workflow',
                        verbose_name='Workflow'
                    )
                ),
            ],
            options={
                'verbose_name': 'Workflow state',
                'verbose_name_plural': 'Workflow states',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkflowTransition',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True,
                        serialize=False, verbose_name='ID'
                    )
                ),
                (
                    'label', models.CharField(
                        max_length=255, verbose_name='Label'
                    )
                ),
                (
                    'destination_state', models.ForeignKey(
                        on_delete=models.CASCADE,
                        related_name='destination_transitions',
                        to='document_states.WorkflowState',
                        verbose_name='Destination state'
                    )
                ),
                (
                    'origin_state', models.ForeignKey(
                        on_delete=models.CASCADE,
                        related_name='origin_transitions',
                        to='document_states.WorkflowState',
                        verbose_name='Origin state'
                    )
                ),
                (
                    'workflow', models.ForeignKey(
                        on_delete=models.CASCADE, related_name='transitions',
                        to='document_states.Workflow',
                        verbose_name='Workflow'
                    )
                ),
            ],
            options={
                'verbose_name': 'Workflow transition',
                'verbose_name_plural': 'Workflow transitions',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='workflowtransition',
            unique_together=set(
                [('workflow', 'label', 'origin_state', 'destination_state')]
            ),
        ),
        migrations.AlterUniqueTogether(
            name='workflowstate',
            unique_together=set([('workflow', 'label')]),
        ),
        migrations.AddField(
            model_name='workflowinstancelogentry',
            name='transition',
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                to='document_states.WorkflowTransition',
                verbose_name='Transition'
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workflowinstancelogentry',
            name='user',
            field=models.ForeignKey(
                on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL,
                verbose_name='User'
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workflowinstancelogentry',
            name='workflow_instance',
            field=models.ForeignKey(
                on_delete=models.CASCADE, related_name='log_entries',
                to='document_states.WorkflowInstance',
                verbose_name='Workflow instance'
            ),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='workflowinstance',
            unique_together=set([('document', 'workflow')]),
        ),
    ]
