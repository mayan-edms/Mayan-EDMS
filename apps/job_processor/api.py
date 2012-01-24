from job_processor.conf.settings import BACKEND


def process_job(func, *args, **kwargs):
    return func(*args, **kwargs)
