# EmployeeHub — Employment Task Management & Performance Tracking System

> **Empower Your Workforce. Measure Performance. Achieve More.**

EmployeeHub is a comprehensive workforce management platform built with Python and Flask. It provides employee management, task tracking, attendance monitoring, performance evaluation, and workforce analytics in one integrated workspace.

![Python](https://img.shields.io/badge/Python-3.x-blue) ![Flask](https://img.shields.io/badge/Flask-3.0-green) ![SQLite](https://img.shields.io/badge/SQLite-3-blue) ![License](https://img.shields.io/badge/License-Academic-orange)

---

## Problem Statement

Many organizations struggle with fragmented workforce management processes:
- Employee records maintained in spreadsheets
- Task tracking scattered across multiple tools
- Performance reviews conducted manually without data
- No centralized attendance monitoring
- Lack of workforce analytics and insights
- Reporting requires manual data compilation

**EmployeeHub** solves these problems by centralizing all workforce management into a single intelligent platform.

---

## Objectives

1. Centralize employee information management
2. Implement task assignment, tracking, and progress monitoring
3. Develop a transparent, weighted performance evaluation system
4. Track daily attendance with comprehensive analytics
5. Generate actionable workforce insights automatically
6. Provide data visualization through interactive charts
7. Support PDF report generation and CSV data export
8. Implement role-based access control (Admin/Employee)

---

## Features

### Core Modules
| Module | Description |
|--------|-------------|
| **Employee Management** | CRUD operations, search, filters, employee profiles |
| **Task Management** | Kanban board, priority levels, status tracking, overdue detection |
| **Performance Tracking** | Weighted scoring algorithm, classifications, historical trends |
| **Attendance Monitoring** | Daily tracking, monthly summaries, department-level analytics |
| **Leaderboard** | Dynamic rankings with badges (Top Performer, Productivity Star) |
| **Workforce Analytics** | Interactive Chart.js charts, department comparisons |
| **Reports & Export** | PDF reports (ReportLab), CSV export (Pandas) |
| **Automated Insights** | Rule-based performance insights from data |

### Additional Features
- Professional landing page with product showcase
- Role-based access (Admin / Employee)
- Dark mode with localStorage persistence
- Responsive design (Desktop, Tablet, Mobile)
- Form validation and error handling
- Custom 404 and 500 error pages

---

## Technology Stack

| Technology | Purpose |
|-----------|---------|
| Python 3 | Backend programming language |
| Flask 3.0 | Web framework |
| SQLite | Database |
| SQLAlchemy | ORM (Object-Relational Mapping) |
| Flask-Login | Authentication & session management |
| Werkzeug | Password hashing |
| Chart.js | Interactive data visualization |
| Bootstrap 5 | UI framework |
| Bootstrap Icons | Icon library |
| ReportLab | PDF report generation |
| Pandas | CSV data export |

---

## Architecture

```
EmployeeHub/
├── app.py                    # Entry point
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── app/
│   ├── __init__.py           # App factory
│   ├── models/               # SQLAlchemy models (7 tables)
│   ├── routes/               # Flask blueprints (8 modules)
│   ├── services/             # Business logic layer
│   ├── utils/                # Helpers, validators, seed data
│   ├── templates/            # Jinja2 templates (15+ pages)
│   └── static/               # CSS, JS, images
└── tests/                    # Test suite
```

---

## Database Design

### Tables and Relationships
| Table | Description | Key Relationships |
|-------|-------------|-------------------|
| `users` | Authentication accounts | FK → employees |
| `employees` | Employee profiles | FK → departments, self-referencing (manager) |
| `departments` | Organization departments | FK → employees (head) |
| `tasks` | Task assignments | FK → employees |
| `performances` | Monthly performance records | FK → employees |
| `attendances` | Daily attendance records | FK → employees |
| `feedbacks` | Employee feedback | FK → employees (receiver, giver) |

---

## Performance Algorithm

EmployeeHub uses a weighted performance scoring formula:

```
Final Score = (Task Completion × 0.30) + (Quality Score × 0.25) +
              (Attendance × 0.15) + (Productivity × 0.20) +
              (Manager Rating × 0.10)
```

### Classifications
| Score Range | Classification |
|-------------|---------------|
| 90 – 100 | Excellent |
| 80 – 89 | Very Good |
| 70 – 79 | Good |
| 60 – 69 | Average |
| Below 60 | Needs Improvement |

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Navigate to project directory:**
   ```bash
   cd "Employee management"
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open in browser:**
   ```
   http://localhost:5000
   ```

The database and demo data are created automatically on first run.

---

## Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| **Admin** | admin@employeehub.com | admin123 |
| **Employee** | arjun.kumar@employeehub.com | employee123 |

---

## Demo Data

The application comes pre-loaded with:
- **5 Departments**: IT, HR, Finance, Marketing, Operations
- **32 Employees** with realistic Indian names
- **100+ Tasks** across all departments
- **6 months of attendance** records
- **Monthly performance** records
- **Feedback** records

---

## Testing

Run the test suite:
```bash
python -m pytest tests/test_app.py -v
```

Tests cover:
- Authentication (login, logout, protected routes)
- Employee CRUD operations
- Task management
- Performance score calculation
- Attendance tracking
- Report generation
- Password security

---

## Future Scope

1. Email notifications for task assignments
2. Calendar view for attendance
3. Employee self-service portal
4. REST API for mobile integration
5. Advanced analytics with ML-based predictions
6. Multi-language support
7. File attachments for tasks
8. Chat/messaging system

---

## Limitations

1. Single-server deployment (SQLite)
2. No real-time notifications
3. No file upload for employee photos
4. Basic role system (Admin/Employee only)
5. No API versioning

---

## Conclusion

EmployeeHub demonstrates a complete, functional workforce management system built with Python and Flask. It showcases database design, algorithmic scoring, data visualization, role-based access control, and modern UI/UX — making it suitable for academic demonstration while maintaining the quality of a commercial application.

---

*Academic Project — Employment Task Management and Performance Tracking System Using Python*
