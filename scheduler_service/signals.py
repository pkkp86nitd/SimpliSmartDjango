from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)


@receiver(post_migrate)
def create_periodic_task(sender, **kwargs):
    logger.info("Post-migrate signal triggered")
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=5, period=IntervalSchedule.SECONDS,
    )
    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name='Scheduled deployment task',
        task='scheduler_service.tasks.process_scheduled_deployments',
    )
    logger.info("Periodic task created successfully")

