from cluster_service.cluster_service import ClusterService
from deployment_service.models import Deployment
from deployment_service.tasks import process_deployment


class SchedulerService:

    def __init__(self):
        pass

    def schedule_deployment(self, user_id, deployment_id):
        deployment = Deployment.objects.get(id=deployment_id)
        cluster_service = ClusterService()

        if deployment.status == 'RUNNING':
            return f"Deployment {deployment.id} already in 'RUNNING' state."
        elif deployment.status == 'QUEUED':
            return f"Deployment {deployment.id} is already in 'QUEUED' state."

        if cluster_service.has_available_resources(deployment.required_cpu, deployment.required_ram, deployment.required_gpu):
            deployment.status = 'RUNNING'
            deployment.save()
            process_deployment.apply_async((deployment.id,))
            return f"Deployment {deployment.id} started successfully."
        else:
            deployment.status = 'QUEUED'
            deployment.save()
            return f"Deployment {deployment.id} queued due to insufficient resources."

    def has_available_resources(self, deployment):
        # Check if cluster resources are available
        cluster_service = ClusterService()
        return cluster_service.has_available_resources(
            deployment.required_cpu,
            deployment.required_ram,
            deployment.required_gpu
        )

    def run_scheduled_deployments(self):
        # Fetch all queued deployments, sorted by priority
        deployments = Deployment.objects.filter(status='QUEUED').order_by('-priority')

        for deployment in deployments:
            self.schedule_deployment(user_id=None, deployment_id=deployment.id)
