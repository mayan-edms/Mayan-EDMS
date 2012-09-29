from __future__ import absolute_import

import os
import datetime
import uuid
import hashlib
import platform
from multiprocessing import Process

import psutil

from django.db import models, IntegrityError, transaction
from django.db import close_connection
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.simplejson import loads, dumps

from clustering.models import Node

from .literals import (JOB_STATE_CHOICES, JOB_STATE_PENDING,
    JOB_STATE_PROCESSING, JOB_STATE_ERROR, WORKER_STATE_CHOICES,
    WORKER_STATE_RUNNING, DEFAULT_JOB_QUEUE_POLL_INTERVAL,
    JOB_QUEUE_STATE_STOPPED, JOB_QUEUE_STATE_STARTED,
    JOB_QUEUE_STATE_CHOICES, DEFAULT_DEAD_JOB_REMOVAL_INTERVAL,
    DEFAULT_JOB_QUEUE_PRIORITY, JOB_QUEUE_ITEM_UNIQUE_ID_TRUNCATE_LENGTH)
from .exceptions import (JobQueuePushError, JobQueueNoPendingJobs,
    JobQueueAlreadyStarted, JobQueueAlreadyStopped)

job_queue_labels = {}
job_types_registry = {}


class Job(object):
    def __init__(self, function, job_queue_item):
        close_connection()
        # Run sync or launch async subprocess
        # OR launch 2 processes: monitor & actual process
        node = Node.objects.myself()
        worker, created = Worker.objects.get_or_create(node=node, pid=os.getpid())
        worker.job_queue_item = job_queue_item
        worker.save()
        try:
            transaction.commit_on_success(function)(**loads(job_queue_item.kwargs))
            #function(**loads(job_queue_item.kwargs))
        except Exception, exc:
            transaction.rollback()
            @transaction.commit_on_success
            def set_state_error():
                job_queue_item.result = exc
                job_queue_item.state = JOB_STATE_ERROR
                try:
                    job_queue_item.save()
                except:
                    transaction.rollback()
                
            set_state_error()
        else:
            job_queue_item.delete()
        finally:
            worker.delete()
            

class JobType(object):
    def __init__(self, name, label, function):
        self.name = name
        self.label = label
        self.function = function
        job_types_registry[self.name] = self
        
    def __unicode__(self):
        return unicode(self.label)
       
    def run(self, job_queue_item, **kwargs):
        job_queue_item.state = JOB_STATE_PROCESSING
        job_queue_item.save()
        p = Process(target=Job, args=(self.function, job_queue_item,))
        p.start()


class JobQueueManager(models.Manager):
    def get_or_create(self, *args, **kwargs):
        job_queue_labels[kwargs.get('name')] = kwargs.get('defaults', {}).get('label')
        return super(JobQueueManager, self).get_or_create(*args, **kwargs)


class JobQueue(models.Model):
    # Internal name
    name = models.CharField(max_length=32, verbose_name=_(u'name'), unique=True)
    unique_jobs = models.BooleanField(verbose_name=_(u'unique jobs'), default=True)
    state = models.CharField(max_length=4,
        choices=JOB_QUEUE_STATE_CHOICES,
        default=JOB_QUEUE_STATE_STARTED,
        verbose_name=_(u'state'))
    priority = models.IntegerField(default=DEFAULT_JOB_QUEUE_PRIORITY, verbose_name=_(u'priority'))
        
    objects = JobQueueManager()

    def __unicode__(self):
        return unicode(self.label) or self.names
        
    @property
    def label(self):
        return job_queue_labels.get(self.name)

    def push(self, job_type, **kwargs):  # TODO: add replace flag
        job_queue_item = JobQueueItem(job_queue=self, job_type=job_type.name, kwargs=dumps(kwargs))
        job_queue_item.save()
        return job_queue_item
        
    #def pull(self):
    #    queue_item_qs = JobQueueItem.objects.filter(queue=self).order_by('-creation_datetime')
    #    if queue_item_qs:
    #        queue_item = queue_item_qs[0]
    #        queue_item.delete()
    #        return loads(queue_item.data)

    def get_oldest_pending_job(self):
        try:
            return self.pending_jobs.all().order_by('-creation_datetime')[0]
        except IndexError:
            raise JobQueueNoPendingJobs

    @property
    def pending_jobs(self):
        return self.items.filter(state=JOB_STATE_PENDING)
    
    @property
    def error_jobs(self):
        return self.items.filter(state=JOB_STATE_ERROR)

    @property
    def active_jobs(self):
        return self.items.filter(state=JOB_STATE_PROCESSING)
        
    @property
    def items(self):
        return self.jobqueueitem_set
        
    def empty(self):
        self.items.all().delete()
        
    def save(self, *args, **kwargs):
        label = getattr(self, 'label', None)
        if label:
            job_queue_labels[self.name] = label
        return super(JobQueue, self).save(*args, **kwargs)

    def stop(self):
        if self.state == JOB_QUEUE_STATE_STOPPED:
            raise JobQueueAlreadyStopped
        
        self.state = JOB_QUEUE_STATE_STOPPED
        self.save()
    
    def start(self):
        if self.state == JOB_QUEUE_STATE_STARTED:
            raise JobQueueAlreadyStarted
        
        self.state = JOB_QUEUE_STATE_STARTED
        self.save()
        
    def is_running(self):
        return self.state == JOB_QUEUE_STATE_STARTED
        
    # TODO: custom runtime methods
        
    class Meta:
        verbose_name = _(u'job queue')
        verbose_name_plural = _(u'job queues')
        ordering = ('priority',)


class JobQueueItemManager(models.Manager):
    def dead_job_queue_items(self):
        return self.model.objects.filter(state=JOB_STATE_PROCESSING).filter(worker__isnull=True)

    def check_dead_job_queue_items(self):
        for job_item in self.dead_job_queue_items():
            job_item.requeue(force=True, at_top=True)


class JobQueueItem(models.Model):
    job_queue = models.ForeignKey(JobQueue, verbose_name=_(u'job queue'))
    creation_datetime = models.DateTimeField(verbose_name=_(u'creation datetime'), editable=False)
    unique_id = models.CharField(blank=True, max_length=64, verbose_name=_(u'id'), unique=True, editable=False)
    job_type = models.CharField(max_length=32, verbose_name=_(u'job type'))
    kwargs = models.TextField(verbose_name=_(u'keyword arguments'))
    state = models.CharField(max_length=4,
        choices=JOB_STATE_CHOICES,
        default=JOB_STATE_PENDING,
        verbose_name=_(u'state'))
    result = models.TextField(blank=True, verbose_name=_(u'result'))

    objects = JobQueueItemManager()

    def __unicode__(self):
        if JOB_QUEUE_ITEM_UNIQUE_ID_TRUNCATE_LENGTH:
            return u'%s...' % self.unique_id[:JOB_QUEUE_ITEM_UNIQUE_ID_TRUNCATE_LENGTH]
        else:
            return self.unique_id
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.creation_datetime = datetime.datetime.now()
            if self.job_queue.unique_jobs:
                self.unique_id = hashlib.sha256(u'%s-%s' % (self.job_type, self.kwargs)).hexdigest()
            else:
                self.unique_id = unicode(uuid.uuid4())

        try:
            super(JobQueueItem, self).save(*args, **kwargs)
        except IntegrityError:
            # TODO: Maybe replace instead of rasining exception w/ replace flag
            raise JobQueuePushError
            
    def get_job_type(self):
        return job_types_registry.get(self.job_type)
            
    def run(self):
        job_type_instance = self.get_job_type()
        job_type_instance.run(self)
        
    @property
    def worker(self):
        try:
            return self.worker_set.get()
        except Worker.DoesNotExist:
            return None
    
    @property
    def is_in_error_state(self):
        return self.state == JOB_STATE_ERROR

    @property
    def is_in_pending_state(self):
        return self.state == JOB_STATE_PENDING

    @property
    def is_in_processing_state(self):
        return self.state == JOB_STATE_PROCESSING


    def requeue(self, force=False, at_top=False):
        """
        Requeue a job so that it is executed again
        force: requeue even if job is not in error state
        at_top: requeue at the top of the file usually for jobs that
            die and shouldn't be placed at the bottom of the queue
        """
        if self.is_in_error_state or force == True:
            # TODO: raise exception if not in error state
            self.state = JOB_STATE_PENDING
            if not at_top:
                self.creation_datetime = datetime.datetime.now()
            self.save()

    class Meta:
        ordering = ('creation_datetime',)
        verbose_name = _(u'job queue item')
        verbose_name_plural = _(u'job queue items')
    

class Worker(models.Model):
    node = models.ForeignKey(Node, verbose_name=_(u'node'))
    pid = models.PositiveIntegerField(max_length=255, verbose_name=_(u'name'))
    creation_datetime = models.DateTimeField(verbose_name=_(u'creation datetime'), default=lambda: datetime.datetime.now(), editable=False)
    heartbeat = models.DateTimeField(blank=True, default=datetime.datetime.now(), verbose_name=_(u'heartbeat check'))
    state = models.CharField(max_length=4,
        choices=WORKER_STATE_CHOICES,
        default=WORKER_STATE_RUNNING,
        verbose_name=_(u'state'))
    job_queue_item = models.ForeignKey(JobQueueItem, blank=True, null=True, verbose_name=_(u'job queue item'))

    def __unicode__(self):
        return u'%s-%s' % (self.node.hostname, self.pid)

    def terminate(self):
        if self.node != Node.objects.myself():
            raise Exception('Not local worker')
            #TODO: dispatch terminate request to remote nodes
        try:
            process = psutil.Process(int(self.pid))
        except psutil.error.NoSuchProcess:
            # Process must have finished before reaching this point
            return
        else:
            process.terminate()

    class Meta:
        ordering = ('creation_datetime',)
        verbose_name = _(u'worker')
        verbose_name_plural = _(u'workers')
        unique_together = ('node', 'pid')
