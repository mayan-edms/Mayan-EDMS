from __future__ import unicode_literals

import logging

from mayan.celery import app

from .classes import StatisticNamespace

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def task_check_statistics():
    logger.info('Executing')

    for namespace in StatisticNamespace.get_all():
        for statistic in namespace.statistics:
            statistic.execute()

    logger.info('Finshed')
