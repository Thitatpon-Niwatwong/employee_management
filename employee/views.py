from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import Employee, Position, Department, Status
from .serializers import (
    EmployeeSerializer,
    PositionSerializer,
    DepartmentSerializer,
    StatusSerializer
)


class StatusViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class PositionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'position', 'department']
    search_fields = ['name', 'address']

# Create your views here.
