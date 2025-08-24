from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Employee, WorkLocation, AttendanceRecord
from .serializers import (
    UserSerializer, EmployeeSerializer, WorkLocationSerializer,
    AttendanceRecordSerializer, AttendanceCreateSerializer
)

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Employee.objects.all()
        return Employee.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def me(self, request):
        try:
            employee = Employee.objects.get(user=request.user)
            serializer = self.get_serializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response(
                {"detail": "Employee profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class WorkLocationViewSet(viewsets.ModelViewSet):
    queryset = WorkLocation.objects.all()
    serializer_class = WorkLocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkLocation.objects.filter(is_active=True)

class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return AttendanceCreateSerializer
        return AttendanceRecordSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return AttendanceRecord.objects.all()
        try:
            employee = Employee.objects.get(user=self.request.user)
            return AttendanceRecord.objects.filter(employee=employee)
        except Employee.DoesNotExist:
            return AttendanceRecord.objects.none()

    @action(detail=False, methods=['get'])
    def today(self, request):
        from django.utils import timezone
        import datetime

        try:
            employee = Employee.objects.get(user=request.user)
            today = timezone.now().date()
            records = AttendanceRecord.objects.filter(
                employee=employee,
                timestamp__date=today
            ).order_by('timestamp')
            
            serializer = AttendanceRecordSerializer(records, many=True)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response(
                {"detail": "Employee profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def mark_attendance(self, request):
        try:
            employee = Employee.objects.get(user=request.user)
            data = request.data.copy()
            data['employee'] = employee.id
            
            serializer = AttendanceCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    AttendanceRecordSerializer(serializer.instance).data,
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response(
                {"detail": "Employee profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )
