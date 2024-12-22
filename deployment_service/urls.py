from django.urls import path
from .views import DeploymentCreateView, DeploymentDetailView

urlpatterns = [
    path('create/', DeploymentCreateView.as_view(), name='create-deployment'),
    path('<int:pk>/', DeploymentDetailView.as_view(), name='deployment-detail'),
]
