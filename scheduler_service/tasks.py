

import logging
from celery import shared_task

from scheduler_service.scheduler_service import SchedulerService

logger = logging.getLogger(__name__)


@shared_task
def process_scheduled_deployments():
    logger.info('Starting the scheduled deployment task...')
    scheduler_service = SchedulerService()
    scheduler_service.run_scheduled_deployments()
    logger.info('Scheduled deployment task completed.')
