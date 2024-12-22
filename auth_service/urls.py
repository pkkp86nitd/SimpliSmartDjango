from django.urls import path
from .views import RegisterUserView, OrganizationInviteView, LoginUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('invite/', OrganizationInviteView.as_view(), name='invite'),
]
