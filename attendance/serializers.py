from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_gis.serializers import GeoFeatureModelSerializer
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

class WorkLocationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = WorkLocation
        geo_field = 'location'
        fields = ('id', 'name', 'address', 'location', 'radius', 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at')

class AttendanceRecordSerializer(GeoFeatureModelSerializer):
    employee_name = serializers.SerializerMethodField()
    work_location_name = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceRecord
        geo_field = 'location'
        fields = ('id', 'employee', 'employee_name', 'timestamp', 'attendance_type', 
                 'location', 'work_location', 'work_location_name', 'status', 'device_info')
        read_only_fields = ('id', 'status')

    def get_employee_name(self, obj):
        return str(obj.employee)

    def get_work_location_name(self, obj):
        return obj.work_location.name

class AttendanceCreateSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = AttendanceRecord
        fields = ('employee', 'attendance_type', 'work_location', 'latitude', 'longitude', 'device_info')

    def create(self, validated_data):
        lat = validated_data.pop('latitude')
        lon = validated_data.pop('longitude')
        validated_data['location'] = Point(lon, lat)
        return AttendanceRecord.objects.create(**validated_data)
