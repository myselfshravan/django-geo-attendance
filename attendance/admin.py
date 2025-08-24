from django.contrib import admin
from .models import Employee, WorkLocation, AttendanceRecord

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'get_full_name', 'department', 'designation')
    search_fields = ('employee_id', 'user__first_name', 'user__last_name', 'department')
    list_filter = ('department', 'designation')

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'

@admin.register(WorkLocation)
class WorkLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'radius', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'address')

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'timestamp', 'attendance_type', 'status', 'work_location')
    list_filter = ('attendance_type', 'status', 'work_location', 'timestamp')
    search_fields = ('employee__employee_id', 'employee__user__first_name', 'employee__user__last_name')
    date_hierarchy = 'timestamp'
    readonly_fields = ('status',)
