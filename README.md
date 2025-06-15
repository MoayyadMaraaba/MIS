# MIS - Human Rights Monitor Management Information System

## 📋 Overview

The **Human Rights Monitor Management Information System (MIS)** is a secure, data-driven platform designed to document, track, and analyze human rights violations. The system provides comprehensive tools for incident reporting, case management, victim tracking, and data analytics.

## 🚀 Features

### Core Functionality
- **Anonymous Incident Reporting** - Secure reporting system with optional anonymity
- **Case Management** - Full lifecycle tracking from investigation to resolution
- **Victim Management** - Demographics, risk assessment, and support services tracking
- **Evidence Management** - File upload and storage for incident documentation
- **Analytics & Reporting** - Data visualization and CSV export capabilities
- **Geographic Tracking** - Location-based incident mapping with coordinates

### User Management
- **Role-based Access Control** - Organizations and Analysts with different permissions
- **JWT Authentication** - Secure token-based authentication system
- **Account Activation** - Admin-controlled user activation workflow

### Analytics Dashboard
- **Violation Type Analysis** - Statistical breakdown of violation categories
- **Timeline Visualization** - Incident trends over time
- **Geographic Distribution** - Map-based incident visualization
- **Data Export** - CSV export for external analysis

## 🏗️ Technical Architecture

### Backend
- **Framework**: FastAPI (Python)
- **Database**: MongoDB
- **Authentication**: JWT with bcrypt password hashing
- **File Storage**: Local filesystem for evidence uploads

### Frontend
- **Technology**: HTML5, CSS3, JavaScript (Vanilla)
- **Design**: Responsive web design with modern UI
- **Architecture**: Multi-page application with role-based interfaces

## 📁 Project Structure

```
MIS/
├── server.py              # FastAPI application entry point
├── config/
│   └── db.py             # MongoDB connection configuration
├── models/
│   ├── User.py           # User data model
│   ├── Case.py           # Case management model
│   └── Incident.py       # Incident reporting model
├── routes/
│   ├── Authentication.py # User auth endpoints
│   ├── Cases.py          # Case management API
│   ├── Incidents.py      # Incident reporting API
│   ├── Victims.py        # Victim management API
│   ├── Admin.py          # Administrative functions
│   └── Analytics.py      # Data analysis endpoints
├── Front/
│   ├── index.html        # Public homepage
│   ├── pages/            # Application pages
│   ├── Styles/           # CSS stylesheets
│   └── images/           # Static assets
├── uploads/
│   └── evidence/         # Evidence file storage
└── utils/
    └── helpers.py        # Utility functions
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- MongoDB
- Node.js (for frontend dependencies, if needed)

### Environment Variables
Create a `.env` file in the root directory:

```env
mongo_uri=mongodb://localhost:27017/
database=mis_database
JWT_SECRET=your_jwt_secret_key
```

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MIS
   ```

2. **Install Python dependencies**
   ```bash
   pip install fastapi uvicorn pymongo python-dotenv bcrypt python-jose python-multipart
   ```

3. **Set up MongoDB**
   - Install and start MongoDB
   - Create database as specified in `.env`

4. **Run the application**
   ```bash
   uvicorn server:app --reload 
   ```

5. **Access the application**
   - Backend API: `http://localhost:8000`
   - Frontend: `http://localhost:5500/Front/index.html`
   - API Documentation: `http://localhost:8000/docs`

## 🔐 User Roles & Permissions

### Organization Role
- Submit incident reports
- Manage cases
- View analytics
- Export data

### Analyst Role
- Advanced analytics access
- Case investigation tools
- Victim management
- Administrative functions

### Admin Role
- Activate/deactivate user accounts
- Access comprehensive system statistics
- Full victim database management
- Case lookup and retrieval
- System oversight and monitoring
- Highest level administrative controls

## 📊 API Endpoints

### Authentication
- `POST /Authentication/Register` - User registration
- `POST /Authentication/Login` - User login

### Authorization
- `GET /Authorization/verify` - Verify JWT token

### Incident Management (Reports)
- `GET /Reports/` - List incidents with filtering
- `POST /Reports/` - Submit new incident report
- `GET /Reports/search` - Search incidents
- `GET /Reports/Count` - Get incident count
- `PATCH /Reports/{report_id}` - Update incident report
- `GET /Reports/analytics` - Incident analytics

### Case Management
- `GET /Cases/` - List cases
- `GET /Cases/{case_id}` - Get case by ID
- `GET /Cases/history/{case_id}` - Get case status history
- `POST /Cases/` - Create new case
- `PATCH /Cases/{case_id}` - Update case
- `DELETE /Cases/{case_id}` - Delete case

### Victim Management
- `GET /Victims/` - List all victims
- `POST /Victims/` - Create new victim record
- `GET /Victims/{victim_id}` - Get victim by ID
- `PATCH /Victims/{victim_id}` - Update victim record
- `GET /Victims/case/{case_id}` - Get victims by case ID

### Analytics
- `GET /analytics/violations` - Violation type statistics
- `GET /analytics/geodata` - Geographic data
- `GET /analytics/timeline` - Timeline analysis
- `GET /analytics/export` - Export data as CSV

### Administration
- `GET /Admin/Count` - System statistics
- `GET /Admin/Users` - List all users
- `PATCH /Admin/User/Activate/{user_id}` - Activate user account
- `GET /Admin/Victims` - Get victim list for admin
- `GET /Admin/case` - Get case information by case ID

## 🗄️ Database Schema

### Collections
- **Users** - User accounts and authentication
- **cases** - Case management records
- **case_archive** - Archived case records
- **case_status_history** - Case status change tracking
- **incident_reports** - Incident submissions
- **report_evidence** - Evidence file metadata
- **victims** - Victim information and tracking

## 🔒 Security Features

- **JWT Token Authentication** - Secure API access
- **Password Hashing** - bcrypt encryption
- **Role-based Access Control** - Permission management
- **CORS Configuration** - Cross-origin request handling
- **File Upload Validation** - Secure evidence storage

## 📈 Analytics Capabilities

- **Violation Type Distribution** - Statistical analysis of violation categories
- **Geographic Mapping** - Location-based incident visualization
- **Temporal Analysis** - Incident trends over time periods
- **Data Export** - CSV format for external analysis tools
- **Real-time Statistics** - Dashboard metrics and counters

## 🔄 Version History

- **v1.0.0** - Initial release with core functionality
  - Incident reporting system
  - Case management
  - User authentication
  - Basic analytics

---

**Note**: This system handles sensitive human rights data. Ensure proper security measures and compliance with data protection regulations in your deployment environment. 
