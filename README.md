# Geo-Tagging Based Attendance System

A Django-based attendance management system that uses geo-tagging to verify employee attendance. This system allows organizations to track employee attendance based on their physical location, ensuring they are within the designated work area when marking attendance.

## Features

- 🌍 Location-based attendance verification
- 🔐 Role-based access control (Admin/HR/Employees)
- 📍 Multiple work location support with geofencing
- 📱 Device information tracking
- 📊 Comprehensive attendance reports
- ✅ Automatic attendance status verification
- 🚀 Serverless deployment support

## Tech Stack

- Django 4.1.3+
- Django REST Framework
- PostgreSQL (Production) / SQLite (Development)
- JWT Authentication
- Vercel (Serverless Deployment)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
# .env file
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=your-secret-key
DEBUG=False
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/token/` - Get JWT tokens
- `POST /api/token/refresh/` - Refresh JWT token

### Employee Management
- `GET /api/employees/` - List employees
- `POST /api/employees/` - Create employee
- `GET /api/employees/me/` - Get current employee details

### Work Locations
- `GET /api/locations/` - List work locations
- `POST /api/locations/` - Add work location (Admin only)
- `PUT /api/locations/{id}/` - Update work location
- `DELETE /api/locations/{id}/` - Delete work location

### Attendance
- `GET /api/attendance/` - List attendance records
- `POST /api/attendance/mark_attendance/` - Mark attendance
- `GET /api/attendance/today/` - Get today's attendance

## API Usage Examples

### Mark Attendance
```json
POST /api/attendance/mark_attendance/
{
    "attendance_type": "CHECK_IN",
    "work_location": 1,
    "latitude": 12.9716,
    "longitude": 77.5946,
    "device_info": {
        "device_id": "iPhone12",
        "platform": "iOS",
        "browser": "Safari"
    }
}
```

### Add Work Location
```json
POST /api/locations/
{
    "name": "Main Office",
    "address": "123 Business Park, City",
    "latitude": 12.9716,
    "longitude": 77.5946,
    "radius": 100,
    "is_active": true
}
```

## Location Verification

The system uses the Haversine formula to calculate the distance between the employee's location and the work location. Attendance is marked as:
- `VERIFIED` - Within work location radius
- `OUTSIDE_RANGE` - Outside work location radius
- `UNVERIFIED` - Location verification failed

## Admin Interface

Access the admin interface at `/admin/` to:
- Manage employees and work locations
- View and filter attendance records
- Generate attendance reports
- Monitor attendance status

## Deployment

This application is optimized for serverless deployment on Vercel:

1. Configure Vercel project
2. Set environment variables in Vercel dashboard
3. Connect to PostgreSQL database
4. Deploy using Vercel CLI or GitHub integration

## License

MIT License - Feel free to use this project for your organization.
