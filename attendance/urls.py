from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'employees', views.EmployeeViewSet)
router.register(r'locations', views.WorkLocationViewSet)
router.register(r'attendance', views.AttendanceRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
