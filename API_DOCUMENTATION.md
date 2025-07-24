# MaintAI Backend API Documentation

## Overview

The MaintAI Backend is a Flask-based REST API that provides comprehensive maintenance management functionality for industrial applications. It includes user authentication, machine monitoring, activity logging, and predictive analytics capabilities.

## Base URL

```
http://localhost:5000/api
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Default Credentials

- **Username**: `admin`
- **Password**: `password`
- **Role**: `admin`

## API Endpoints

### Authentication Endpoints

#### POST /auth/login
Authenticate a user and receive a JWT token.

**Request Body:**
```json
{
  "username": "admin",
  "password": "password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@maintai.com",
    "role": "admin",
    "created_at": "2025-07-24T23:11:49.224280",
    "is_active": true
  }
}
```

#### POST /auth/register
Register a new user.

**Request Body:**
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "password123",
  "role": "technician"
}
```

#### GET /auth/me
Get current user information (requires authentication).

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@maintai.com",
    "role": "admin",
    "created_at": "2025-07-24T23:11:49.224280",
    "is_active": true
  }
}
```

### Machine Management Endpoints

#### GET /machines/
Get all machines (requires authentication).

**Response:**
```json
[
  {
    "id": "MACHINE-001",
    "name": "Production Line A",
    "status": "operational",
    "efficiency": 85.0,
    "temperature": 35.0,
    "vibration": 0.4,
    "lastMaintenance": "2024-01-15",
    "created_at": "2025-07-24T23:13:33.739168",
    "updated_at": "2025-07-24T23:13:33.739171"
  }
]
```

#### POST /machines/
Create a new machine (requires authentication).

**Request Body:**
```json
{
  "id": "MACHINE-005",
  "name": "New Production Line",
  "status": "operational",
  "efficiency": 100.0,
  "temperature": 25.0,
  "vibration": 0.5,
  "last_maintenance": "2024-01-20"
}
```

#### GET /machines/{machine_id}
Get a specific machine by ID (requires authentication).

#### PUT /machines/{machine_id}
Update a machine (requires authentication).

#### DELETE /machines/{machine_id}
Delete a machine (requires authentication).

#### POST /machines/generate-sample
Generate sample machines for testing (requires authentication).

**Response:**
```json
{
  "message": "Created 4 sample machines",
  "machines": ["MACHINE-001", "MACHINE-002", "MACHINE-003", "MACHINE-004"]
}
```

### Activity Management Endpoints

#### GET /activities/
Get all activities (requires authentication).

#### POST /activities/
Create a new activity (requires authentication).

**Request Body:**
```json
{
  "description": "Routine maintenance check",
  "technician": "John Doe",
  "status": "pending",
  "machine_id": "MACHINE-001"
}
```

#### GET /activities/{activity_id}
Get a specific activity by ID (requires authentication).

#### PUT /activities/{activity_id}
Update an activity (requires authentication).

#### DELETE /activities/{activity_id}
Delete an activity (requires authentication).

#### POST /activities/generate-sample
Generate sample activities for testing (requires authentication).

### Analytics Endpoints

#### GET /analytics/dashboard-stats
Get dashboard statistics (requires authentication).

**Response:**
```json
{
  "total_machines": 4,
  "operational_machines": 2,
  "warning_machines": 1,
  "maintenance_machines": 1,
  "avg_efficiency": 81.8,
  "recent_activities": 0,
  "total_cost_savings": 0
}
```

#### GET /analytics/predictive
Get predictive analytics data for all machines (requires authentication).

#### GET /analytics/maintenance-schedule
Get maintenance schedule recommendations (requires authentication).

**Response:**
```json
[
  {
    "machineId": "MACHINE-004",
    "machineName": "Packaging Unit D",
    "urgency": "high",
    "recommendedDays": 3,
    "estimatedCost": 2500,
    "currentStatus": "maintenance"
  }
]
```

#### GET /analytics/cost-analysis
Get cost analysis data (requires authentication).

#### POST /analytics/generate-sample-data
Generate sample predictive data for testing (requires authentication).

## Error Responses

All endpoints return appropriate HTTP status codes and error messages:

```json
{
  "error": "Error description"
}
```

Common status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `500`: Internal Server Error

## Database Models

### User
- `id`: Integer (Primary Key)
- `username`: String (Unique)
- `email`: String (Unique)
- `password_hash`: String
- `role`: String (admin, technician, guest)
- `created_at`: DateTime
- `is_active`: Boolean

### Machine
- `id`: String (Primary Key)
- `name`: String
- `status`: String (operational, warning, maintenance)
- `efficiency`: Float
- `temperature`: Float
- `vibration`: Float
- `last_maintenance`: String
- `created_at`: DateTime
- `updated_at`: DateTime

### Activity
- `id`: Integer (Primary Key)
- `description`: String
- `technician`: String
- `status`: String (pending, in-progress, completed, active)
- `machine_id`: String (Foreign Key)
- `timestamp`: DateTime
- `completed_at`: DateTime

### PredictiveData
- `id`: Integer (Primary Key)
- `machine_id`: String (Foreign Key)
- `failure_probability`: Float
- `recommended_maintenance`: Integer (days)
- `cost_savings`: Float
- `created_at`: DateTime
- `updated_at`: DateTime

## CORS Configuration

The API is configured to accept requests from any origin (`*`) for development purposes. In production, this should be restricted to specific domains.

## Security Features

- JWT-based authentication
- Password hashing using bcrypt
- Role-based access control
- CORS protection
- Input validation

## Development Setup

1. Navigate to the project directory
2. Activate the virtual environment: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the server: `python src/main.py`

The server will start on `http://0.0.0.0:5000` with debug mode enabled.

