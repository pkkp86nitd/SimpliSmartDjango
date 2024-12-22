from django.contrib import admin
from .models import Cluster

class ClusterAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_cpu', 'total_ram', 'total_gpu', 'used_cpu', 'used_ram', 'used_gpu')
    search_fields = ('name',)
    list_filter = ('name',)

admin.site.register(Cluster, ClusterAdmin)
