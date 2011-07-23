from scheduler import scheduler

registered_jobs = {}


def register_interval_job(func, weeks=0, days=0, hours=0, minutes=0,
                         seconds=0, start_date=None, args=None,
                         kwargs=None, job_name=None, **options):

    scheduler.add_interval_job(func=func, weeks=weeks, days=days,
        hours=hours, minutes=minutes, seconds=seconds,
        start_date=start_date, args=args, kwargs=kwargs)#, **options)
