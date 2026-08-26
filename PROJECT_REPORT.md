# PROJECT REPORT

## Employment Task Management and Performance Tracking System Using Python

### Product Name: EmployeeHub

---

## 1. Abstract

EmployeeHub is a web-based Employment Task Management and Performance Tracking System developed using Python and Flask. The system addresses the challenges of fragmented workforce management by providing a centralized platform for employee management, task tracking, attendance monitoring, performance evaluation, and workforce analytics. The application implements a weighted performance scoring algorithm, generates automated insights from workforce data, and supports PDF report generation and CSV data export. Built with a modular architecture, the system demonstrates core software engineering principles including database design, authentication, role-based access control, algorithmic computation, and responsive user interface design.

**Keywords:** Employee Management, Task Management, Performance Tracking, Python, Flask, SQLAlchemy, Data Visualization, Workforce Analytics

---

## 2. Introduction

Effective workforce management is critical to organizational success. Traditional approaches relying on spreadsheets, manual tracking, and paper-based processes are prone to errors, lack visibility, and make data-driven decisions difficult. EmployeeHub addresses these challenges by providing an integrated digital platform that brings together employee records, task assignments, attendance tracking, performance evaluation, and analytics into a single workspace.

The system is designed to serve as a demonstration of modern web application development using Python, showcasing both technical implementation skills and practical problem-solving capabilities.

---

## 3. Problem Statement

Organizations face several challenges in workforce management:

1. **Fragmented Data**: Employee information spread across multiple spreadsheets and tools
2. **Manual Task Tracking**: No centralized system for task assignment and progress monitoring
3. **Subjective Performance Reviews**: Performance evaluations based on perception rather than measurable data
4. **Attendance Gaps**: Difficulty tracking attendance patterns and their impact on productivity
5. **Reporting Overhead**: Significant manual effort required to compile workforce reports
6. **No Analytics**: Lack of workforce visibility and data-driven decision-making capabilities

---

## 4. Existing System

Current workforce management in many organizations involves:
- Microsoft Excel for employee records
- Email for task assignment and tracking
- Manual attendance registers
- Annual subjective performance reviews
- Manual report compilation

**Limitations of Existing System:**
- Data inconsistency and duplication
- No real-time progress visibility
- Time-consuming manual processes
- Lack of performance metrics
- No automated insights or analytics

---

## 5. Proposed System

EmployeeHub is a web-based application that provides:
- Centralized employee information management
- Digital task management with Kanban boards
- Daily attendance tracking and monitoring
- Algorithmic performance scoring using weighted metrics
- Interactive workforce analytics and visualizations
- Automated report generation (PDF) and data export (CSV)
- Role-based access control for data security
- Automated performance insights from workforce data

---

## 6. Objectives

1. Design and implement a comprehensive employee management module with CRUD operations
2. Develop a task management system with status tracking and Kanban visualization
3. Create a transparent, weighted performance evaluation algorithm
4. Implement daily attendance tracking with monthly summaries
5. Build interactive analytics dashboards using Chart.js
6. Generate professional PDF reports using ReportLab
7. Implement authentication and role-based authorization
8. Create a responsive, professional user interface

---

## 7. Scope

**In Scope:**
- Employee CRUD management
- Task assignment, tracking, and Kanban visualization
- Weighted performance scoring algorithm
- Attendance tracking (Present, Absent, Leave, Late)
- Interactive data visualization
- PDF report generation
- CSV data export
- Role-based access (Admin/Employee)
- Dark mode
- Responsive design

**Out of Scope:**
- Payroll processing
- Leave management workflows
- Real-time chat/messaging
- Mobile native applications
- Multi-tenancy

---

## 8. Methodology

The project follows an incremental development methodology with the following phases:

1. **Requirements Analysis** — Define functional and non-functional requirements
2. **Database Design** — Design entity relationships and SQLAlchemy models
3. **Backend Development** — Implement Flask routes, services, and business logic
4. **Frontend Development** — Create templates with responsive CSS and JavaScript
5. **Integration Testing** — Verify all components work together
6. **Documentation** — Prepare project documentation and user guides

---

## 9. Requirements

### 9.1 Functional Requirements

| ID | Requirement |
|----|------------|
| FR-01 | System shall allow user authentication (login/logout) |
| FR-02 | System shall support role-based access (Admin/Employee) |
| FR-03 | Admin shall be able to create, read, update, and deactivate employees |
| FR-04 | Admin shall be able to create, assign, and manage tasks |
| FR-05 | System shall track task status (To Do, In Progress, Under Review, Completed, Overdue) |
| FR-06 | System shall calculate performance scores using a weighted algorithm |
| FR-07 | System shall track daily attendance |
| FR-08 | System shall generate dynamic leaderboards |
| FR-09 | System shall display interactive analytics charts |
| FR-10 | System shall generate PDF reports |
| FR-11 | System shall export data to CSV |
| FR-12 | System shall provide search and filtering capabilities |

### 9.2 Non-Functional Requirements

| ID | Requirement |
|----|------------|
| NFR-01 | Passwords must be hashed (not stored in plaintext) |
| NFR-02 | Application must be responsive across devices |
| NFR-03 | System must support dark mode |
| NFR-04 | Application must run locally without external dependencies |
| NFR-05 | Database operations must use ORM (no raw SQL) |

---

## 10. System Architecture

The application follows a Model-View-Controller (MVC) pattern implemented through Flask:

- **Models** (app/models/): SQLAlchemy ORM models defining database schema
- **Views** (app/templates/): Jinja2 HTML templates for presentation
- **Controllers** (app/routes/): Flask blueprints handling HTTP requests
- **Services** (app/services/): Business logic layer for complex operations

---

## 11. Database Design

### 11.1 Tables

| Table | Columns | Purpose |
|-------|---------|---------|
| users | id, email, password_hash, role, employee_id | Authentication |
| employees | id, employee_code, first_name, last_name, email, phone, department_id, designation, date_of_joining, manager_id, status | Employee records |
| departments | id, name, code, description, head_id | Department structure |
| tasks | id, title, description, employee_id, priority, status, due_date, progress, quality_score | Task management |
| performances | id, employee_id, period, task_completion, quality_score, attendance_score, productivity_score, manager_rating, final_score, classification | Performance records |
| attendances | id, employee_id, date, status, check_in, check_out | Attendance records |
| feedbacks | id, employee_id, given_by, type, content | Feedback records |

### 11.2 Relationships
- Users → Employees (One-to-One)
- Employees → Departments (Many-to-One)
- Employees → Employees (Self-referencing: Manager)
- Tasks → Employees (Many-to-One)
- Performances → Employees (Many-to-One)
- Attendances → Employees (Many-to-One)
- Feedbacks → Employees (Many-to-One, both receiver and giver)

---

## 12. Algorithms

### 12.1 Performance Scoring Algorithm

```python
def calculate_performance_score(task_completion, quality_score,
                                 attendance_score, productivity_score,
                                 manager_rating):
    final_score = (
        task_completion * 0.30 +    # 30% weight
        quality_score * 0.25 +       # 25% weight
        attendance_score * 0.15 +    # 15% weight
        productivity_score * 0.20 +  # 20% weight
        manager_rating * 0.10        # 10% weight
    )
    # Classification based on score range
    if final_score >= 90: classification = "Excellent"
    elif final_score >= 80: classification = "Very Good"
    elif final_score >= 70: classification = "Good"
    elif final_score >= 60: classification = "Average"
    else: classification = "Needs Improvement"
    return final_score, classification
```

### 12.2 Automated Insight Generation

The system generates rule-based insights by analyzing:
- Top performer identification
- Productivity trend comparison (current vs. previous period)
- Low performance threshold detection
- Deadline risk assessment
- Attendance rate monitoring
- Department performance comparison

---

## 13. Implementation

### 13.1 Technology Stack
- **Backend:** Python 3, Flask 3.0
- **Database:** SQLite with SQLAlchemy ORM
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Charts:** Chart.js 4.x
- **Reports:** ReportLab
- **Data Export:** Pandas

### 13.2 Key Implementation Details
- Flask Application Factory pattern for modular design
- Blueprint-based route organization (8 blueprints)
- Service layer for business logic separation
- Werkzeug password hashing for security
- Flask-Login for session management
- CSS custom properties for theming (dark mode)

---

## 14. Testing

The project includes a comprehensive test suite (tests/test_app.py) covering:
- Authentication flow (login, logout, protected routes)
- Employee CRUD operations
- Task creation and status updates
- Performance score calculations (all 5 classifications)
- Attendance marking
- PDF report generation
- CSV export functionality
- Password security verification

---

## 15. Results

The system successfully implements:
- ✅ Complete employee management with 32 demo records
- ✅ Task management with Kanban board and 100+ demo tasks
- ✅ Weighted performance scoring algorithm
- ✅ 6 months of attendance data with tracking
- ✅ Dynamic leaderboard with rankings
- ✅ Interactive analytics with Chart.js
- ✅ PDF report generation
- ✅ CSV data export
- ✅ Role-based access control
- ✅ Dark mode support
- ✅ Responsive design

---

## 16. Limitations

1. Uses SQLite (not suitable for concurrent production use)
2. No real-time notification system
3. No file upload capability for employee photos
4. Two-role system only (Admin and Employee)
5. No API versioning for external integrations

---

## 17. Future Scope

1. Email notification system for task assignments and deadlines
2. Calendar-based attendance visualization
3. Employee self-service portal for profile management
4. RESTful API for mobile application integration
5. Machine learning-based performance prediction
6. Multi-language internationalization support
7. Integration with external HR systems
8. Automated report scheduling and distribution

---

## 18. Conclusion

EmployeeHub successfully demonstrates a complete employment task management and performance tracking system built with Python. The project showcases practical application of web development concepts including database design, algorithmic computation, data visualization, authentication, and responsive UI design. The weighted performance scoring algorithm provides objective employee evaluation, while interactive analytics enable data-driven workforce decisions. The modular architecture ensures maintainability and extensibility, making the system suitable for both academic demonstration and practical adoption.

---

*Project Report — Employment Task Management and Performance Tracking System Using Python*
*Technology: Python • Flask • SQLAlchemy • SQLite • Chart.js • ReportLab • Pandas*
