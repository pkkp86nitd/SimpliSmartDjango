from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class SchedulerServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler_service'

    def ready(self):
        logger.info("Scheduler Service is being initialized.")
        try:
            import scheduler_service.signals  # Try to import signals lazily
            logger.info("Signals successfully imported.")
        except ImportError as e:
            logger.error(f"Error importing signals: {e}")
