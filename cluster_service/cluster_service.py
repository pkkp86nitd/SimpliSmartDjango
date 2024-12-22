from cluster_service.models import Cluster


class ClusterService:
    CPU_WEIGHT = 1.0
    RAM_WEIGHT = 0.4
    GPU_WEIGHT = 25.0

    def __init__(self):
        pass

    def has_available_resources(self, required_cpu, required_ram, required_gpu):
        """
        Checks if any cluster has sufficient resources to handle the deployment.
        """
        clusters = Cluster.objects.all()  # Fetch all clusters
        for cluster in clusters:
            if (
                cluster.total_cpu - cluster.used_cpu >= required_cpu and
                cluster.total_ram - cluster.used_ram >= required_ram and
                cluster.total_gpu - cluster.used_gpu >= required_gpu
            ):
                return True
        return False

    def allocate_resources(self, required_cpu, required_ram, required_gpu):
        """
        Allocates resources from the cluster with the most available capacity
        using a weighted utilization algorithm.
        """
        clusters = Cluster.objects.all()

        def calculate_weighted_score(cluster):
            available_cpu = cluster.total_cpu - cluster.used_cpu
            available_ram = cluster.total_ram - cluster.used_ram
            available_gpu = cluster.total_gpu - cluster.used_gpu

            # Weighted score based on available resources
            return (
                available_cpu * self.CPU_WEIGHT +
                available_ram * self.RAM_WEIGHT +
                available_gpu * self.GPU_WEIGHT
            )

        # Sort clusters by their weighted score in descending order
        clusters = sorted(clusters, key=calculate_weighted_score, reverse=True)

        for cluster in clusters:
            if (
                cluster.total_cpu - cluster.used_cpu >= required_cpu and
                cluster.total_ram - cluster.used_ram >= required_ram and
                cluster.total_gpu - cluster.used_gpu >= required_gpu
            ):
                # Allocate resources
                cluster.used_cpu += required_cpu
                cluster.used_ram += required_ram
                cluster.used_gpu += required_gpu
                cluster.save()
                return cluster.id  # Return the ID of the allocated cluster

        raise ValueError("Insufficient resources in all clusters to allocate.")

    def free_resources(self, required_cpu, required_ram, required_gpu, cluster_id=None):
        """
        Frees resources from the specified cluster or the one that matches the requirement.
        """
        clusters = Cluster.objects.filter(id=cluster_id) if cluster_id else Cluster.objects.all()

        for cluster in clusters:
            if (
                cluster.used_cpu >= required_cpu and
                cluster.used_ram >= required_ram and
                cluster.used_gpu >= required_gpu
            ):
                # Free resources
                cluster.used_cpu -= required_cpu
                cluster.used_ram -= required_ram
                cluster.used_gpu -= required_gpu
                cluster.save()
                return cluster.id  # Return the ID of the cluster freed

        raise ValueError("Unable to free resources due to mismatch or insufficient usage.")
