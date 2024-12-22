from django.db import models


class Cluster(models.Model):
    name = models.CharField(max_length=255)
    total_cpu = models.FloatField()
    total_ram = models.FloatField()
    total_gpu = models.FloatField()
    used_cpu = models.FloatField(default=0)
    used_ram = models.FloatField(default=0)
    used_gpu = models.FloatField(default=0)

    def has_available_resources(self, required_cpu, required_ram, required_gpu):
        return (
                self.total_cpu - self.used_cpu >= required_cpu and
                self.total_ram - self.used_ram >= required_ram and
                self.total_gpu - self.used_gpu >= required_gpu
        )

    def allocate_resources(self, required_cpu, required_ram, required_gpu):
        self.used_cpu += required_cpu
        self.used_ram += required_ram
        self.used_gpu += required_gpu
        self.save()

    def free_resources(self, required_cpu, required_ram, required_gpu):
        self.used_cpu -= required_cpu
        self.used_ram -= required_ram
        self.used_gpu -= required_gpu
        self.save()
