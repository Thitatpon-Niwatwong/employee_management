from rest_framework import serializers
from .models import Employee, Position, Department, Status


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=Status.objects.all(), source='status', write_only=True
    )
    image = serializers.ImageField(required=False)

    class Meta:
        model = Employee
        fields = '__all__'
