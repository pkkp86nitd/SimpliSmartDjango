from unittest.mock import patch, MagicMock
from django.test import TestCase
from scheduler_service.scheduler_service import SchedulerService
from deployment_service.models import Deployment
from deployment_service.tasks import process_deployment


class TestSchedulerService(TestCase):

    @patch('scheduler_service.scheduler_service.ClusterService')
    @patch('deployment_service.models.Deployment.objects.get')
    @patch('deployment_service.tasks.process_deployment.apply_async')  # Mock Celery task here
    def test_schedule_deployment_with_available_resources(self, mock_apply_async, mock_get, MockClusterService):
        # Create a mock deployment
        deployment = MagicMock(spec=Deployment)
        deployment.id = 1
        deployment.status = 'PENDING'
        deployment.required_cpu = 2
        deployment.required_ram = 4
        deployment.required_gpu = 1

        # Mock the `get()` method to return the mocked deployment
        mock_get.return_value = deployment

        # Mock the ClusterService to return True for available resources
        mock_cluster_service = MockClusterService.return_value
        mock_cluster_service.has_available_resources.return_value = True

        # Create the scheduler service
        scheduler_service = SchedulerService()

        # Call the method
        result = scheduler_service.schedule_deployment(user_id=None, deployment_id=deployment.id)

        # Check that the deployment status is set to 'RUNNING'
        deployment.status = 'RUNNING'
        deployment.save.assert_called_once()

        # Check if the process_deployment task is called asynchronously
        mock_apply_async.assert_called_once_with((deployment.id,))

        # Validate the result
        self.assertEqual(result, f"Deployment {deployment.id} started successfully.")

    @patch('scheduler_service.scheduler_service.ClusterService')
    @patch('deployment_service.models.Deployment.objects.get')
    @patch('deployment_service.tasks.process_deployment.apply_async')  # Mock Celery task here
    def test_schedule_deployment_with_insufficient_resources(self, mock_apply_async, mock_get, MockClusterService):
        # Create a mock deployment
        deployment = MagicMock(spec=Deployment)
        deployment.id = 2
        deployment.status = 'PENDING'
        deployment.required_cpu = 2
        deployment.required_ram = 4
        deployment.required_gpu = 1

        # Mock the `get()` method to return the mocked deployment
        mock_get.return_value = deployment

        # Mock the ClusterService to return False for available resources
        mock_cluster_service = MockClusterService.return_value
        mock_cluster_service.has_available_resources.return_value = False

        # Create the scheduler service
        scheduler_service = SchedulerService()

        # Call the method
        result = scheduler_service.schedule_deployment(user_id=None, deployment_id=deployment.id)

        # Check that the deployment status is set to 'QUEUED'
        deployment.status = 'QUEUED'
        deployment.save.assert_called_once()

        # Validate the result
        self.assertEqual(result, f"Deployment {deployment.id} queued due to insufficient resources.")

    @patch('scheduler_service.scheduler_service.ClusterService')
    @patch('deployment_service.models.Deployment.objects.get')
    @patch('deployment_service.tasks.process_deployment.apply_async')  # Mock Celery task here
    def test_schedule_deployment_when_deployment_is_running(self, mock_apply_async, mock_get, MockClusterService):
        # Create a mock deployment in 'RUNNING' state
        deployment = MagicMock(spec=Deployment)
        deployment.id = 3
        deployment.status = 'RUNNING'
        deployment.required_cpu = 2
        deployment.required_ram = 4
        deployment.required_gpu = 1

        # Mock the `get()` method to return the mocked deployment
        mock_get.return_value = deployment

        # Create the scheduler service
        scheduler_service = SchedulerService()

        # Call the method
        result = scheduler_service.schedule_deployment(user_id=None, deployment_id=deployment.id)

        # Ensure that no changes happen to the deployment (status should remain 'RUNNING')
        deployment.save.assert_not_called()

        # Validate the result
        self.assertEqual(result, f"Deployment {deployment.id} already in 'RUNNING' state.")

    @patch('scheduler_service.scheduler_service.ClusterService')
    @patch('deployment_service.models.Deployment.objects.get')
    @patch('deployment_service.tasks.process_deployment.apply_async')  # Mock Celery task here
    def test_schedule_deployment_when_deployment_is_queued(self, mock_apply_async, mock_get, MockClusterService):
        # Create a mock deployment in 'QUEUED' state
        deployment = MagicMock(spec=Deployment)
        deployment.id = 4
        deployment.status = 'QUEUED'
        deployment.required_cpu = 2
        deployment.required_ram = 4
        deployment.required_gpu = 1

        # Mock the `get()` method to return the mocked deployment
        mock_get.return_value = deployment

        # Create the scheduler service
        scheduler_service = SchedulerService()

        # Call the method
        result = scheduler_service.schedule_deployment(user_id=None, deployment_id=deployment.id)

        # Ensure that no changes happen to the deployment (status should remain 'QUEUED')
        deployment.save.assert_not_called()

        # Validate the result
        self.assertEqual(result, f"Deployment {deployment.id} is already in 'QUEUED' state.")
