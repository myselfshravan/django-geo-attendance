from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Employee, WorkLocation, AttendanceRecord

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = ('id', 'user', 'employee_id', 'department', 'designation', 'profile_photo')
        read_only_fields = ('id',)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee

class WorkLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkLocation
        fields = ('id', 'name', 'address', 'latitude', 'longitude', 'radius', 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at')

class AttendanceRecordSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    work_location_name = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceRecord
        fields = ('id', 'employee', 'employee_name', 'timestamp', 'attendance_type', 
                 'latitude', 'longitude', 'work_location', 'work_location_name', 
                 'status', 'device_info')
        read_only_fields = ('id', 'status')

    def get_employee_name(self, obj):
        return str(obj.employee)

    def get_work_location_name(self, obj):
        return obj.work_location.name

class AttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = ('employee', 'attendance_type', 'work_location', 'latitude', 'longitude', 'device_info')
