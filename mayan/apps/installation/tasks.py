from mayan.celery import app

from .models import Installation


@app.task
def task_details_submit():
    details = Installation.objects.get()
    details.submit()
