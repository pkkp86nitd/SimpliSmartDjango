from django.db import models
from django.utils import timezone
from cluster_service.models import Cluster


class Deployment(models.Model):
    docker_image = models.CharField(max_length=255)
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    required_cpu = models.FloatField()
    required_ram = models.FloatField()
    required_gpu = models.FloatField()
    priority = models.IntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=[('QUEUED', 'Queued'), ('RUNNING', 'Running'), ('FAILED', 'Failed'), ('COMPLETED', 'Completed')],
        default='QUEUED'
    )
    created_at = models.DateTimeField(default=timezone.now)
    retry_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Deployment {self.id} - {self.docker_image}"


