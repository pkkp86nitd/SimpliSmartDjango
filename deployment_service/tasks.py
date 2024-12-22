from celery import shared_task
from cluster_service.cluster_service import ClusterService
from .models import Deployment


@shared_task
def process_deployment(deployment_id):
    deployment = Deployment.objects.get(id=deployment_id)
    cluster_service = ClusterService()

    try:
        if cluster_service.has_available_resources(
                deployment.required_cpu,
                deployment.required_ram,
                deployment.required_gpu):
            # Allocate resources
            cluster_service.allocate_resources(
                deployment.required_cpu,
                deployment.required_ram,
                deployment.required_gpu
            )

            deployment.status = 'RUNNING'
            deployment.save()

            #  deployment logic here
            # For example, deploying the code, starting containers, etc.

            deployment.status = 'COMPLETED'
            deployment.save()

        else:
            # Retry logic if resources are insufficient
            deployment.retry_count += 1
            deployment.save()

            if deployment.retry_count < 3:
                # Retry the deployment after a delay (5 minutes)
                process_deployment.apply_async((deployment_id,), countdown=300)
            else:
                deployment.status = 'FAILED'
                deployment.save()


    except Exception as e:
        #  any unexpected error, mark the deployment as failed
        deployment.status = 'FAILED'
        deployment.save()
        print(f"Error processing deployment {deployment_id}: {e}")
