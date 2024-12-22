from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Cluster
from .serializers import ClusterSerializer


class ClusterList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List all clusters.
        """
        clusters = Cluster.objects.all()
        serializer = ClusterSerializer(clusters, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new cluster.
        """
        serializer = ClusterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClusterDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """
        Retrieve a cluster by ID.
        """
        try:
            cluster = Cluster.objects.get(pk=pk)
        except Cluster.DoesNotExist:
            return Response({"error": "Cluster not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClusterSerializer(cluster)
        return Response(serializer.data)

    def put(self, request, pk=None):
        """
        Update an existing cluster.
        """
        try:
            cluster = Cluster.objects.get(pk=pk)
        except Cluster.DoesNotExist:
            return Response({"error": "Cluster not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClusterSerializer(cluster, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """
        Delete a cluster.
        """
        try:
            cluster = Cluster.objects.get(pk=pk)
        except Cluster.DoesNotExist:
            return Response({"error": "Cluster not found."}, status=status.HTTP_404_NOT_FOUND)

        cluster.delete()
        return Response({"message": "Cluster deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class CheckResources(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        """
        Check if a cluster has enough resources available.
        """
        try:
            cluster = Cluster.objects.get(pk=pk)
        except Cluster.DoesNotExist:
            return Response({"error": "Cluster not found."}, status=status.HTTP_404_NOT_FOUND)

        required_cpu = request.data.get("required_cpu", 0)
        required_ram = request.data.get("required_ram", 0)
        required_gpu = request.data.get("required_gpu", 0)

        if cluster.has_available_resources(required_cpu, required_ram, required_gpu):
            return Response({"message": "Resources are available."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Not enough resources."}, status=status.HTTP_400_BAD_REQUEST)


class AllocateResources(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk=None):
        """
        Allocate resources to the cluster.
        """
        try:
            cluster = Cluster.objects.get(pk=pk)
        except Cluster.DoesNotExist:
            return Response({"error": "Cluster not found."}, status=status.HTTP_404_NOT_FOUND)

        required_cpu = request.data.get("required_cpu", 0)
        required_ram = request.data.get("required_ram", 0)
        required_gpu = request.data.get("required_gpu", 0)

        if cluster.has_available_resources(required_cpu, required_ram, required_gpu):
            cluster.allocate_resources(required_cpu, required_ram, required_gpu)
            return Response({"message": "Resources allocated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Not enough resources to allocate."}, status=status.HTTP_400_BAD_REQUEST)


class FreeResources(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk=None):
        """
        Free up resources from the cluster.
        """
        try:
            cluster = Cluster.objects.get(pk=pk)
        except Cluster.DoesNotExist:
            return Response({"error": "Cluster not found."}, status=status.HTTP_404_NOT_FOUND)

        required_cpu = request.data.get("required_cpu", 0)
        required_ram = request.data.get("required_ram", 0)
        required_gpu = request.data.get("required_gpu", 0)

        if cluster.used_cpu >= required_cpu and cluster.used_ram >= required_ram and cluster.used_gpu >= required_gpu:
            cluster.free_resources(required_cpu, required_ram, required_gpu)
            return Response({"message": "Resources freed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Cannot free more resources than currently allocated."},
                            status=status.HTTP_400_BAD_REQUEST)
