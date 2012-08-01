from __future__ import absolute_import

import logging

from apscheduler.scheduler import Scheduler as OriginalScheduler

from django.utils.translation import ugettext_lazy as _

from .exceptions import AlreadyScheduled, UnknownJobClass

logger = logging.getLogger(__name__)


class SchedulerJobBase(object):
    job_type = u''

    def __init__(self, name, label, function, *args, **kwargs):
        self.scheduler = None
        self.name = name
        self.label = label
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.scheduler.stop_job(self)

    @property
    def running(self):
        if self.scheduler:
            return self.scheduler.running
        else:
            return False

    @property
    def start_date(self):
        return self._job.trigger.start_date


class IntervalJob(SchedulerJobBase):
    job_type = _(u'Interval job')

    def start(self, scheduler):
        scheduler.add_job(self)


class DateJob(SchedulerJobBase):
    job_type = _(u'Date job')

    def start(self, scheduler):
        scheduler.add_job(self)


class LocalScheduler(object):
    scheduler_registry = {}
    _lockdown = False

    @classmethod
    def get(cls, name):
        return cls.scheduler_registry[name]

    @classmethod
    def get_all(cls):
        return cls.scheduler_registry.values()

    @classmethod
    def shutdown_all(cls):
        for scheduler in cls.scheduler_registry.values():
            scheduler.stop()

    @classmethod
    def lockdown(cls):
        cls._lockdown = True

    @classmethod
    def clear_all(cls):
        for scheduler in cls.scheduler_registry.values():
            scheduler.clear()

    def __init__(self, name, label=None):
        self.scheduled_jobs = {}
        self._scheduler = None
        self.name = name
        self.label = label
        self.__class__.scheduler_registry[self.name] = self

    def start(self):
        logger.debug('starting scheduler: %s' % self.name)
        if not self.__class__._lockdown:
            self._scheduler = OriginalScheduler()
            for job in self.scheduled_jobs.values():
                self._schedule_job(job)

            self._scheduler.start()
        else:
            logger.debug('lockdown in effect')

    def stop(self):
        if self._scheduler:
            self._scheduler.shutdown()
            del self._scheduler
            self._scheduler = None

    @property
    def running(self):
        if self._scheduler:
            return self._scheduler.running
        else:
            return False

    def clear(self):
        for job in self.scheduled_jobs.values():
            self.stop_job(job)

    def stop_job(self, job):
        if self.running:
            self._scheduler.unschedule_job(job._job)

        del(self.scheduled_jobs[job.name])
        job.scheduler = None

    def _schedule_job(self, job):
        if isinstance(job, IntervalJob):
            job._job = self._scheduler.add_interval_job(job.function, *job.args, **job.kwargs)
        elif isinstance(job, DateJob):
            job._job = self._scheduler.add_date_job(job.function, *job.args, **job.kwargs)
        else:
            raise UnknownJobClass

    def add_job(self, job):
        if job.scheduler or job.name in self.scheduled_jobs.keys():
            raise AlreadyScheduled

        if self._scheduler:
            self._scheduler_job(job)

        job.scheduler = self
        self.scheduled_jobs[job.name] = job

    def add_interval_job(self, name, label, function, *args, **kwargs):
        job = IntervalJob(name=name, label=label, function=function, *args, **kwargs)
        self.add_job(job)
        return job

    def add_date_job(self, name, label, function, *args, **kwargs):
        job = DateJob(name=name, label=label, function=function, *args, **kwargs)
        self.add_job(job)
        return job

    def get_job_list(self):
        return self.scheduled_jobs.values()

    def __unicode__(self):
        return unicode(self.label or self.name)
