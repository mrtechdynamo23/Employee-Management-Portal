"""
EmployeeHub Test Suite
Tests core functionality including authentication, CRUD operations,
performance calculations, and report generation.
"""
import unittest
import os
import sys
from datetime import date, datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.user import User
from app.models.employee import Employee
from app.models.department import Department
from app.models.task import Task
from app.models.performance import Performance
from app.models.attendance import Attendance
from app.services.performance_service import calculate_performance_score


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test-secret-key'
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class BaseTestCase(unittest.TestCase):
    """Base test case with app and database setup."""

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        # Create test data
        self.create_test_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def create_test_data(self):
        """Create minimal test data."""
        # Admin user
        self.admin = User(email='admin@test.com', role='ADMIN')
        self.admin.set_password('admin123')
        db.session.add(self.admin)

        # Department
        self.dept = Department(name='Test Department', code='TEST', description='Test')
        db.session.add(self.dept)
        db.session.flush()

        # Employee
        self.employee = Employee(
            employee_code='EMP001',
            first_name='Test',
            last_name='User',
            email='test@test.com',
            department_id=self.dept.id,
            designation='Developer',
            status='Active',
            avatar_color='#6366F1'
        )
        db.session.add(self.employee)
        db.session.flush()

        # Employee user
        self.emp_user = User(email='test@test.com', role='EMPLOYEE', employee_id=self.employee.id)
        self.emp_user.set_password('emp123')
        db.session.add(self.emp_user)

        db.session.commit()

    def login_admin(self):
        return self.client.post('/login', data={
            'email': 'admin@test.com',
            'password': 'admin123'
        }, follow_redirects=True)

    def login_employee(self):
        return self.client.post('/login', data={
            'email': 'test@test.com',
            'password': 'emp123'
        }, follow_redirects=True)


class TestAuthentication(BaseTestCase):
    """Test authentication flow."""

    def test_landing_page(self):
        """Test landing page loads at root."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'EmployeeHub', response.data)

    def test_login_page(self):
        """Test login page renders."""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome Back', response.data)

    def test_login_success(self):
        """Test successful login."""
        response = self.login_admin()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    def test_login_invalid(self):
        """Test invalid login."""
        response = self.client.post('/login', data={
            'email': 'wrong@test.com',
            'password': 'wrong'
        }, follow_redirects=True)
        self.assertIn(b'Invalid email or password', response.data)

    def test_logout(self):
        """Test logout."""
        self.login_admin()
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_protected_route(self):
        """Test that dashboard requires login."""
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn(b'login', response.data.lower())


class TestEmployeeCRUD(BaseTestCase):
    """Test employee management."""

    def test_employee_list(self):
        """Test employee list page."""
        self.login_admin()
        response = self.client.get('/employees/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)

    def test_add_employee(self):
        """Test adding a new employee."""
        self.login_admin()
        response = self.client.post('/employees/add', data={
            'first_name': 'New',
            'last_name': 'Employee',
            'email': 'new@test.com',
            'phone': '+91-12345-67890',
            'department_id': self.dept.id,
            'designation': 'Tester'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        emp = Employee.query.filter_by(email='new@test.com').first()
        self.assertIsNotNone(emp)
        self.assertEqual(emp.full_name, 'New Employee')

    def test_edit_employee(self):
        """Test editing an employee."""
        self.login_admin()
        response = self.client.post(f'/employees/{self.employee.id}/edit', data={
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'test@test.com',
            'designation': 'Senior Developer'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        emp = Employee.query.get(self.employee.id)
        self.assertEqual(emp.first_name, 'Updated')

    def test_deactivate_employee(self):
        """Test deactivating an employee."""
        self.login_admin()
        response = self.client.post(f'/employees/{self.employee.id}/deactivate', follow_redirects=True)
        emp = Employee.query.get(self.employee.id)
        self.assertEqual(emp.status, 'Inactive')

    def test_employee_detail(self):
        """Test employee detail page."""
        self.login_admin()
        response = self.client.get(f'/employees/{self.employee.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)


class TestTaskManagement(BaseTestCase):
    """Test task management."""

    def test_create_task(self):
        """Test creating a task."""
        self.login_admin()
        response = self.client.post('/tasks/add', data={
            'title': 'Test Task',
            'description': 'A test task description',
            'employee_id': self.employee.id,
            'priority': 'High',
            'due_date': '2026-12-31'
        }, follow_redirects=True)
        task = Task.query.filter_by(title='Test Task').first()
        self.assertIsNotNone(task)
        self.assertEqual(task.priority, 'High')
        self.assertEqual(task.status, 'To Do')

    def test_update_task(self):
        """Test updating a task."""
        self.login_admin()
        task = Task(
            title='Update Me',
            employee_id=self.employee.id,
            priority='Medium',
            status='To Do'
        )
        db.session.add(task)
        db.session.commit()

        response = self.client.post(f'/tasks/{task.id}/update', data={
            'title': 'Updated Task',
            'status': 'In Progress',
            'progress': 50,
            'priority': 'High'
        }, follow_redirects=True)
        updated = Task.query.get(task.id)
        self.assertEqual(updated.status, 'In Progress')
        self.assertEqual(updated.progress, 50)

    def test_task_status_api(self):
        """Test task status update API."""
        self.login_admin()
        task = Task(title='API Task', employee_id=self.employee.id, priority='Medium', status='To Do')
        db.session.add(task)
        db.session.commit()

        response = self.client.post(f'/tasks/{task.id}/status',
            json={'status': 'Completed'},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        updated = Task.query.get(task.id)
        self.assertEqual(updated.status, 'Completed')


class TestPerformanceCalculation(BaseTestCase):
    """Test performance scoring algorithm."""

    def test_excellent_score(self):
        """Test Excellent classification (90-100)."""
        score, classification = calculate_performance_score(95, 92, 98, 90, 94)
        self.assertEqual(classification, 'Excellent')
        self.assertGreaterEqual(score, 90)

    def test_very_good_score(self):
        """Test Very Good classification (80-89)."""
        score, classification = calculate_performance_score(85, 82, 88, 80, 84)
        self.assertEqual(classification, 'Very Good')
        self.assertGreaterEqual(score, 80)
        self.assertLess(score, 90)

    def test_good_score(self):
        """Test Good classification (70-79)."""
        score, classification = calculate_performance_score(75, 72, 78, 70, 74)
        self.assertEqual(classification, 'Good')

    def test_average_score(self):
        """Test Average classification (60-69)."""
        score, classification = calculate_performance_score(65, 62, 68, 60, 64)
        self.assertEqual(classification, 'Average')

    def test_needs_improvement(self):
        """Test Needs Improvement classification (<60)."""
        score, classification = calculate_performance_score(50, 45, 55, 40, 50)
        self.assertEqual(classification, 'Needs Improvement')
        self.assertLess(score, 60)

    def test_specific_score_calculation(self):
        """Test specific score: Arjun Kumar example from landing page."""
        score, classification = calculate_performance_score(92, 95, 97, 91, 94)
        # (92*0.30) + (95*0.25) + (97*0.15) + (91*0.20) + (94*0.10)
        # = 27.6 + 23.75 + 14.55 + 18.2 + 9.4 = 93.5
        expected = round(92*0.30 + 95*0.25 + 97*0.15 + 91*0.20 + 94*0.10, 1)
        self.assertEqual(score, expected)
        self.assertEqual(classification, 'Excellent')

    def test_clamping(self):
        """Test that values are clamped between 0-100."""
        score, _ = calculate_performance_score(150, -10, 200, 50, 50)
        self.assertLessEqual(score, 100)


class TestPerformanceRoutes(BaseTestCase):
    """Test performance tracking web routes."""

    def test_admin_performance_page(self):
        """Test admin performance page loads."""
        self.login_admin()
        response = self.client.get('/performance/')
        self.assertEqual(response.status_code, 200)

    def test_employee_performance_page(self):
        """Test employee scorecard page loads."""
        self.login_employee()
        response = self.client.get('/performance/')
        self.assertEqual(response.status_code, 200)

    def test_leaderboard_page(self):
        """Test leaderboard page loads."""
        self.login_admin()
        response = self.client.get('/performance/leaderboard')
        self.assertEqual(response.status_code, 200)


class TestAttendance(BaseTestCase):
    """Test attendance tracking."""

    def test_mark_attendance(self):
        """Test marking attendance."""
        self.login_admin()
        response = self.client.post('/attendance/mark', data={
            'employee_id': self.employee.id,
            'date': date.today().isoformat(),
            'status': 'Present',
            'check_in': '09:00',
            'check_out': '18:00'
        }, follow_redirects=True)
        att = Attendance.query.filter_by(
            employee_id=self.employee.id,
            date=date.today()
        ).first()
        self.assertIsNotNone(att)
        self.assertEqual(att.status, 'Present')

    def test_attendance_page(self):
        """Test attendance page loads."""
        self.login_admin()
        response = self.client.get('/attendance/')
        self.assertEqual(response.status_code, 200)


class TestReports(BaseTestCase):
    """Test report generation."""

    def test_reports_page(self):
        """Test reports page loads."""
        self.login_admin()
        response = self.client.get('/reports/')
        self.assertEqual(response.status_code, 200)

    def test_employee_pdf_report(self):
        """Test employee PDF report generation."""
        self.login_admin()
        response = self.client.get('/reports/pdf/employee')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/pdf')

    def test_csv_export_employees(self):
        """Test CSV export for employees."""
        self.login_admin()
        response = self.client.get('/reports/csv/employees')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/csv', response.content_type)


class TestPasswordSecurity(BaseTestCase):
    """Test password security."""

    def test_password_hashing(self):
        """Test that passwords are hashed, not stored in plaintext."""
        user = User.query.filter_by(email='admin@test.com').first()
        self.assertNotEqual(user.password_hash, 'admin123')
        self.assertTrue(user.check_password('admin123'))
        self.assertFalse(user.check_password('wrong'))

    def test_user_roles(self):
        """Test user role assignments."""
        admin = User.query.filter_by(email='admin@test.com').first()
        emp = User.query.filter_by(email='test@test.com').first()
        self.assertTrue(admin.is_admin)
        self.assertFalse(emp.is_admin)


class TestRoleDifferential(BaseTestCase):
    """Test differential experience between Admin and Employee roles."""

    def test_employee_workspace_dashboard(self):
        """Test employee gets personalized workspace dashboard."""
        self.login_employee()
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back', response.data)
        self.assertIn(b'My Active Tasks', response.data)

    def test_employee_check_in(self):
        """Test employee can punch in attendance."""
        self.login_employee()
        response = self.client.post('/attendance/check-in', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        att = Attendance.query.filter_by(employee_id=self.employee.id, date=date.today()).first()
        self.assertIsNotNone(att)

    def test_employee_restricted_admin_routes(self):
        """Test that employees cannot access admin-only pages."""
        self.login_employee()
        # Employees cannot access employee directory
        emp_response = self.client.get('/employees/')
        self.assertEqual(emp_response.status_code, 403)

        # Employees cannot access full reports
        rep_response = self.client.get('/reports/')
        self.assertEqual(rep_response.status_code, 403)

        # Employees cannot access org-wide analytics
        analytics_response = self.client.get('/analytics/')
        self.assertEqual(analytics_response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
