# MaintAI Backend Setup Instructions

## Overview

This Flask backend provides a complete API for the MaintAI maintenance management system. It includes user authentication, machine monitoring, activity logging, and predictive analytics capabilities.

## Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- Git (optional, for version control)

## Quick Start

### 1. Navigate to the Project Directory
```bash
cd maintai-backend
```

### 2. Activate the Virtual Environment
```bash
source venv/bin/activate
```

### 3. Install Dependencies (if needed)
```bash
pip install -r requirements.txt
```

### 4. Start the Development Server
```bash
python src/main.py
```

The server will start on `http://0.0.0.0:5000` with debug mode enabled.

## Default Login Credentials

- **Username**: `admin`
- **Password**: `password`
- **Role**: `admin`

## Testing the API

### 1. Login and Get Token
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

### 2. Generate Sample Data
```bash
# Use the token from login response
curl -X POST http://localhost:5000/api/machines/generate-sample \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 3. Get Machines List
```bash
curl -X GET http://localhost:5000/api/machines/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 4. Get Dashboard Statistics
```bash
curl -X GET http://localhost:5000/api/analytics/dashboard-stats \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Database Configuration

### Current Setup (SQLite)
The backend currently uses SQLite for development, which requires no additional setup. The database file is automatically created at `src/database/app.db`.

### PostgreSQL Setup (Production)
To use PostgreSQL in production:

1. Install PostgreSQL and create a database
2. Set the `DATABASE_URL` environment variable:
   ```bash
   export DATABASE_URL="postgresql://username:password@localhost/maintai_db"
   ```
3. The application will automatically use PostgreSQL when the environment variable is set

## Environment Variables

Create a `.env` file in the project root for production settings:

```env
DATABASE_URL=postgresql://username:password@localhost/maintai_db
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
FLASK_ENV=production
```

## Project Structure

```
maintai-backend/
├── src/
│   ├── models/
│   │   ├── user.py              # User model and authentication
│   │   ├── machine.py           # Machine model
│   │   ├── activity.py          # Activity model
│   │   └── predictive_data.py   # Predictive analytics model
│   ├── routes/
│   │   ├── auth.py              # Authentication endpoints
│   │   ├── user.py              # User management endpoints
│   │   ├── machines.py          # Machine management endpoints
│   │   ├── activities.py        # Activity management endpoints
│   │   └── analytics.py         # Analytics and dashboard endpoints
│   ├── static/                  # Static files (for frontend integration)
│   ├── database/
│   │   └── app.db              # SQLite database file
│   └── main.py                 # Main application entry point
├── venv/                       # Virtual environment
├── requirements.txt            # Python dependencies
├── API_DOCUMENTATION.md        # Complete API documentation
└── SETUP_INSTRUCTIONS.md       # This file
```

## Key Features

### ✅ Implemented Features
- **User Authentication**: JWT-based login/logout system
- **Machine Management**: CRUD operations for industrial machines
- **Activity Logging**: Track maintenance activities and technician work
- **Predictive Analytics**: AI-powered maintenance predictions
- **Dashboard Statistics**: Real-time system overview
- **Maintenance Scheduling**: Optimized maintenance recommendations
- **Cost Analysis**: Financial impact tracking
- **CORS Support**: Cross-origin requests enabled
- **Role-based Access**: Admin, technician, and guest roles
- **Sample Data Generation**: Testing utilities

### 🔧 Technical Features
- **Database Models**: SQLAlchemy ORM with relationship mapping
- **Password Security**: Bcrypt hashing for user passwords
- **JWT Tokens**: Secure authentication with configurable expiration
- **Error Handling**: Comprehensive error responses
- **Input Validation**: Request data validation
- **Auto-migrations**: Database schema updates on startup

## Integration with Frontend

The backend is designed to work seamlessly with the MaintAI React frontend. Key integration points:

1. **Authentication**: Login endpoint returns JWT token for frontend storage
2. **Machine Data**: Real-time machine status updates
3. **Dashboard**: Statistics endpoint provides all dashboard metrics
4. **Activities**: Activity management for maintenance tracking
5. **Analytics**: Predictive insights for maintenance planning

## Deployment Considerations

### Development
- Uses SQLite database (no external dependencies)
- Debug mode enabled
- CORS allows all origins
- Detailed error messages

### Production Recommendations
- Switch to PostgreSQL database
- Disable debug mode
- Restrict CORS to specific domains
- Use environment variables for secrets
- Implement proper logging
- Use a production WSGI server (e.g., Gunicorn)

## Troubleshooting

### Common Issues

1. **Database Errors**: Delete `src/database/app.db` and restart to recreate
2. **Port Already in Use**: Change port in `main.py` or kill existing process
3. **JWT Errors**: Ensure token is included in Authorization header as `Bearer <token>`
4. **CORS Issues**: Check that CORS is properly configured for your frontend domain

### Logs and Debugging
- Server logs are displayed in the terminal
- Debug mode provides detailed error traces
- Check `server.log` if running in background

## Support

For technical support or questions about the API implementation, refer to:
- `API_DOCUMENTATION.md` for complete endpoint documentation
- Database models in `src/models/` for data structure
- Route implementations in `src/routes/` for business logic

## Next Steps

1. **Test the API** using the provided curl commands
2. **Generate sample data** for development and testing
3. **Integrate with frontend** using the authentication flow
4. **Configure production database** when ready for deployment
5. **Customize business logic** as needed for your specific requirements

