from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmployeeViewSet,
    DepartmentViewSet,
    PositionViewSet,
    StatusViewSet
)
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'statuses', StatusViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='api_token_auth'),
]
