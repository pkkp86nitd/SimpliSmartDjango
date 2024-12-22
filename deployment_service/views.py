# deployment_service/views.py
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from scheduler_service.scheduler_service import SchedulerService
from .serializers import DeploymentSerializer
from .models import Deployment


class DeploymentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DeploymentSerializer(data=request.data)
        if serializer.is_valid():
            deployment = serializer.save()
            scheduler_service = SchedulerService()
            result = scheduler_service.schedule_deployment(
                user_id=request.user.id, deployment_id=deployment.id
            )
            return Response(
                {"message": result, "id": deployment.id},
                status=status.HTTP_202_ACCEPTED if deployment.status == 'QUEUED' else status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeploymentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        deployment = get_object_or_404(Deployment, pk=pk)
        serializer = DeploymentSerializer(deployment)
        return Response(serializer.data, status=status.HTTP_200_OK)
