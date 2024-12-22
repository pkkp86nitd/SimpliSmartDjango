from django.contrib import admin
from .models import Deployment


class DeploymentAdmin(admin.ModelAdmin):
    list_display = (
    'docker_image', 'cluster', 'required_cpu', 'required_ram', 'required_gpu', 'status', 'priority', 'created_at')
    search_fields = ('docker_image', 'status', 'cluster__name')
    list_filter = ('status', 'priority', 'cluster')


admin.site.register(Deployment, DeploymentAdmin)
