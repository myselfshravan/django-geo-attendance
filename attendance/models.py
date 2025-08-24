from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import math

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"

class WorkLocation(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField(help_text="Radius in meters")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class AttendanceRecord(models.Model):
    ATTENDANCE_TYPES = (
        ('CHECK_IN', 'Check In'),
        ('CHECK_OUT', 'Check Out'),
    )

    STATUS_CHOICES = (
        ('VERIFIED', 'Verified'),
        ('UNVERIFIED', 'Unverified'),
        ('OUTSIDE_RANGE', 'Outside Range'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    attendance_type = models.CharField(max_length=10, choices=ATTENDANCE_TYPES)
    latitude = models.FloatField()
    longitude = models.FloatField()
    work_location = models.ForeignKey(WorkLocation, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UNVERIFIED')
    device_info = models.JSONField(null=True, blank=True)
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        R = 6371000  # Earth's radius in meters
        φ1 = math.radians(lat1)
        φ2 = math.radians(lat2)
        Δφ = math.radians(lat2 - lat1)
        Δλ = math.radians(lon2 - lon1)

        a = (math.sin(Δφ/2) * math.sin(Δφ/2) +
             math.cos(φ1) * math.cos(φ2) *
             math.sin(Δλ/2) * math.sin(Δλ/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c  # Distance in meters
    
    def save(self, *args, **kwargs):
        if not self.status:
            # Calculate distance between check-in location and work location
            distance = self.calculate_distance(
                self.latitude, 
                self.longitude,
                self.work_location.latitude,
                self.work_location.longitude
            )
            if distance <= self.work_location.radius:
                self.status = 'VERIFIED'
            else:
                self.status = 'OUTSIDE_RANGE'
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.employee} - {self.attendance_type} at {self.timestamp}"
