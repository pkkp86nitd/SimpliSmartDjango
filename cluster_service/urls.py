from django.urls import path
from .views import ClusterList, ClusterDetail, CheckResources, AllocateResources, FreeResources

urlpatterns = [
    path('', ClusterList.as_view(), name='cluster-list'),
    path('<int:pk>/', ClusterDetail.as_view(), name='cluster-detail'),
    path('<int:pk>/check_resources/', CheckResources.as_view(), name='check_resources'),
    path('<int:pk>/allocate_resources/', AllocateResources.as_view(), name='allocate_resources'),
    path('<int:pk>/free_resources/', FreeResources.as_view(), name='free_resources'),
]
