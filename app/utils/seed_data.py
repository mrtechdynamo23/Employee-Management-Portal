"""
Seed data generator for EmployeeHub demo.
Creates realistic demonstration data including employees, tasks, attendance, performance, and feedback.
"""
import random
from datetime import datetime, date, timedelta
from app import db
from app.models.user import User
from app.models.employee import Employee
from app.models.department import Department
from app.models.task import Task
from app.models.performance import Performance
from app.models.attendance import Attendance
from app.models.feedback import Feedback
from app.services.performance_service import calculate_performance_score
from app.utils.helpers import generate_avatar_color


# Employee data
EMPLOYEES = [
    {'first': 'Arjun', 'last': 'Kumar', 'designation': 'Senior Developer', 'dept': 'IT'},
    {'first': 'Priya', 'last': 'Sharma', 'designation': 'HR Manager', 'dept': 'HR'},
    {'first': 'Rahul', 'last': 'Verma', 'designation': 'Financial Analyst', 'dept': 'FIN'},
    {'first': 'Sneha', 'last': 'Rao', 'designation': 'Marketing Lead', 'dept': 'MKT'},
    {'first': 'Karthik', 'last': 'Raj', 'designation': 'Operations Manager', 'dept': 'OPS'},
    {'first': 'Ananya', 'last': 'Iyer', 'designation': 'Frontend Developer', 'dept': 'IT'},
    {'first': 'Vivek', 'last': 'Menon', 'designation': 'Backend Developer', 'dept': 'IT'},
    {'first': 'Meera', 'last': 'Nair', 'designation': 'HR Executive', 'dept': 'HR'},
    {'first': 'Rohan', 'last': 'Kapoor', 'designation': 'Account Manager', 'dept': 'FIN'},
    {'first': 'Divya', 'last': 'Krishnan', 'designation': 'Content Strategist', 'dept': 'MKT'},
    {'first': 'Aditya', 'last': 'Singh', 'designation': 'DevOps Engineer', 'dept': 'IT'},
    {'first': 'Neha', 'last': 'Patel', 'designation': 'Recruiter', 'dept': 'HR'},
    {'first': 'Suresh', 'last': 'Reddy', 'designation': 'Tax Analyst', 'dept': 'FIN'},
    {'first': 'Lakshmi', 'last': 'Devi', 'designation': 'Brand Manager', 'dept': 'MKT'},
    {'first': 'Ajay', 'last': 'Mishra', 'designation': 'Supply Chain Lead', 'dept': 'OPS'},
    {'first': 'Pooja', 'last': 'Gupta', 'designation': 'QA Engineer', 'dept': 'IT'},
    {'first': 'Sanjay', 'last': 'Tiwari', 'designation': 'Payroll Specialist', 'dept': 'HR'},
    {'first': 'Ritu', 'last': 'Agarwal', 'designation': 'Budget Analyst', 'dept': 'FIN'},
    {'first': 'Deepak', 'last': 'Joshi', 'designation': 'SEO Specialist', 'dept': 'MKT'},
    {'first': 'Kavita', 'last': 'Bhatt', 'designation': 'Logistics Coordinator', 'dept': 'OPS'},
    {'first': 'Manish', 'last': 'Chauhan', 'designation': 'Full Stack Developer', 'dept': 'IT'},
    {'first': 'Swati', 'last': 'Kulkarni', 'designation': 'Training Manager', 'dept': 'HR'},
    {'first': 'Vikram', 'last': 'Malhotra', 'designation': 'Audit Analyst', 'dept': 'FIN'},
    {'first': 'Nisha', 'last': 'Desai', 'designation': 'Social Media Manager', 'dept': 'MKT'},
    {'first': 'Rajesh', 'last': 'Pandey', 'designation': 'Warehouse Manager', 'dept': 'OPS'},
    {'first': 'Anjali', 'last': 'Saxena', 'designation': 'UI/UX Designer', 'dept': 'IT'},
    {'first': 'Amit', 'last': 'Sinha', 'designation': 'Compliance Officer', 'dept': 'HR'},
    {'first': 'Tanvi', 'last': 'Mehta', 'designation': 'Revenue Analyst', 'dept': 'FIN'},
    {'first': 'Gaurav', 'last': 'Yadav', 'designation': 'Campaign Manager', 'dept': 'MKT'},
    {'first': 'Sunita', 'last': 'Rajan', 'designation': 'Procurement Lead', 'dept': 'OPS'},
    {'first': 'Harsh', 'last': 'Bansal', 'designation': 'Data Engineer', 'dept': 'IT'},
    {'first': 'Pallavi', 'last': 'Chandra', 'designation': 'Benefits Coordinator', 'dept': 'HR'},
]


# Task templates
TASK_TEMPLATES = {
    'IT': [
        'Implement user authentication module',
        'Fix critical bug in payment gateway',
        'Design database schema for new feature',
        'Optimize API response time',
        'Write unit tests for core modules',
        'Deploy application to staging server',
        'Code review for sprint deliverables',
        'Update API documentation',
        'Migrate legacy database tables',
        'Implement caching layer',
        'Set up CI/CD pipeline',
        'Refactor frontend components',
        'Integrate third-party analytics SDK',
        'Performance testing and optimization',
        'Security vulnerability assessment',
        'Mobile responsive design updates',
        'Implement notification system',
        'Database backup automation',
        'Create admin dashboard widgets',
        'API rate limiting implementation',
    ],
    'HR': [
        'Process new employee onboarding',
        'Update employee handbook',
        'Conduct quarterly performance reviews',
        'Organize team building event',
        'Review compensation benchmarks',
        'Process leave applications',
        'Update HR policy documents',
        'Conduct exit interviews',
        'Organize training workshop',
        'Review health insurance plans',
        'Process payroll adjustments',
        'Create recruitment campaign',
        'Employee satisfaction survey',
        'Update compliance training materials',
        'Review diversity and inclusion metrics',
    ],
    'FIN': [
        'Prepare quarterly financial report',
        'Reconcile monthly bank statements',
        'Process vendor invoices',
        'Audit expense reports',
        'Update budget forecasts',
        'Tax filing preparation',
        'Review capital expenditure requests',
        'Accounts receivable follow-up',
        'Prepare cash flow analysis',
        'Annual audit preparation',
        'Review financial compliance',
        'Process reimbursement claims',
        'Update financial projections',
        'Cost optimization analysis',
        'Revenue tracking report',
    ],
    'MKT': [
        'Create social media content calendar',
        'Design product launch campaign',
        'Analyze website traffic metrics',
        'Prepare marketing budget proposal',
        'A/B test email campaigns',
        'Create promotional materials',
        'SEO optimization for landing pages',
        'Influencer partnership outreach',
        'Customer feedback analysis',
        'Brand guidelines update',
        'Market research report',
        'Competitor analysis report',
        'Content strategy planning',
        'Event marketing coordination',
        'PR and media outreach',
    ],
    'OPS': [
        'Optimize warehouse layout',
        'Review supply chain efficiency',
        'Implement inventory tracking system',
        'Vendor performance evaluation',
        'Quality control audit',
        'Process improvement documentation',
        'Fleet management optimization',
        'Safety compliance inspection',
        'Logistics cost analysis',
        'Delivery schedule optimization',
        'Equipment maintenance planning',
        'Procurement process review',
        'Capacity planning analysis',
        'Standard operating procedure update',
        'Disaster recovery plan review',
    ]
}

FEEDBACK_TEMPLATES = {
    'Appreciation': [
        'Excellent work on the recent project delivery. Your dedication was outstanding.',
        'Great job handling the client presentation. Very professional and well-prepared.',
        'Your leadership during the sprint was commendable. Team morale was noticeably higher.',
        'Outstanding problem-solving skills demonstrated during the critical issue resolution.',
        'Appreciated your proactive approach to identifying and fixing potential risks.',
    ],
    'Improvement': [
        'Could improve on time management — some tasks were delivered past their deadlines.',
        'Documentation could be more detailed. Consider adding examples for complex processes.',
        'Communication with cross-functional teams needs improvement for better coordination.',
        'Would benefit from more thorough testing before submitting deliverables.',
        'Consider prioritizing tasks more effectively during high-workload periods.',
    ],
    'General': [
        'Good overall contribution to the team this quarter.',
        'Consistent performance across all assigned responsibilities.',
        'Positive attitude and willingness to help colleagues is noted.',
        'Shows good potential for growth in the current role.',
        'Reliable team member who meets expectations consistently.',
    ]
}


def seed_all():
    """Seed all demo data."""
    print("  Creating departments...")
    departments = seed_departments()
    print("  Creating employees...")
    employees = seed_employees(departments)
    print("  Creating admin user...")
    seed_admin_user()
    print("  Creating employee user accounts...")
    seed_employee_users(employees)
    print("  Creating tasks...")
    seed_tasks(employees, departments)
    print("  Creating attendance records...")
    seed_attendance(employees)
    print("  Creating performance records...")
    seed_performance(employees)
    print("  Creating feedback...")
    seed_feedback(employees)
    print("  Setting department heads...")
    set_department_heads(departments, employees)
    db.session.commit()


def seed_departments():
    """Create departments."""
    dept_data = [
        {'name': 'Information Technology', 'code': 'IT', 'description': 'Software development, infrastructure, and technical innovation.'},
        {'name': 'Human Resources', 'code': 'HR', 'description': 'Talent acquisition, employee relations, and organizational development.'},
        {'name': 'Finance', 'code': 'FIN', 'description': 'Financial planning, accounting, and budget management.'},
        {'name': 'Marketing', 'code': 'MKT', 'description': 'Brand management, digital marketing, and market research.'},
        {'name': 'Operations', 'code': 'OPS', 'description': 'Supply chain, logistics, and operational excellence.'},
    ]

    departments = {}
    for d in dept_data:
        dept = Department(name=d['name'], code=d['code'], description=d['description'])
        db.session.add(dept)
        departments[d['code']] = dept

    db.session.flush()
    return departments


def seed_employees(departments):
    """Create employees."""
    employees = []
    dept_managers = {}

    for i, emp_data in enumerate(EMPLOYEES):
        dept = departments[emp_data['dept']]
        join_date = date.today() - timedelta(days=random.randint(180, 1200))

        emp = Employee(
            employee_code=f'EMP{str(i + 1).zfill(3)}',
            first_name=emp_data['first'],
            last_name=emp_data['last'],
            email=f"{emp_data['first'].lower()}.{emp_data['last'].lower()}@employeehub.com",
            phone=f"+91-{random.randint(70000, 99999)}-{random.randint(10000, 99999)}",
            department_id=dept.id,
            designation=emp_data['designation'],
            date_of_joining=join_date,
            status='Active',
            avatar_color=generate_avatar_color()
        )
        db.session.add(emp)
        employees.append(emp)

        # First employee of each dept is the manager
        if emp_data['dept'] not in dept_managers:
            dept_managers[emp_data['dept']] = emp

    db.session.flush()

    # Set managers
    for emp in employees:
        dept_code = None
        for code, dept in departments.items():
            if dept.id == emp.department_id:
                dept_code = code
                break
        if dept_code and dept_managers.get(dept_code) and dept_managers[dept_code].id != emp.id:
            emp.manager_id = dept_managers[dept_code].id

    db.session.flush()
    return employees


def seed_admin_user():
    """Create admin user account."""
    admin = User(
        email='admin@employeehub.com',
        role='ADMIN'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.flush()


def seed_employee_users(employees):
    """Create user accounts for some employees."""
    for emp in employees[:5]:
        user = User(
            email=emp.email,
            role='EMPLOYEE',
            employee_id=emp.id
        )
        user.set_password('employee123')
        db.session.add(user)
    db.session.flush()


def seed_tasks(employees, departments):
    """Create tasks for employees."""
    dept_code_map = {}
    for code, dept in departments.items():
        dept_code_map[dept.id] = code

    statuses = ['To Do', 'In Progress', 'Under Review', 'Completed', 'Completed', 'Completed']
    priorities = ['Low', 'Medium', 'Medium', 'High', 'High', 'Critical']

    today = date.today()

    for emp in employees:
        dept_code = dept_code_map.get(emp.department_id, 'IT')
        templates = TASK_TEMPLATES.get(dept_code, TASK_TEMPLATES['IT'])
        num_tasks = random.randint(3, 6)

        selected_tasks = random.sample(templates, min(num_tasks, len(templates)))

        for title in selected_tasks:
            status = random.choice(statuses)
            priority = random.choice(priorities)
            due_offset = random.randint(-30, 45)
            due_date = today + timedelta(days=due_offset)
            created_at = datetime.now() - timedelta(days=random.randint(30, 120))

            progress = 0
            completed_at = None
            quality_score = None

            if status == 'Completed':
                progress = 100
                completed_at = created_at + timedelta(days=random.randint(5, 25))
                quality_score = round(random.uniform(70, 100), 1)
            elif status == 'In Progress':
                progress = random.randint(20, 80)
            elif status == 'Under Review':
                progress = random.randint(80, 95)

            # Mark as overdue if past due date and not completed
            if status != 'Completed' and due_date < today:
                status = 'Overdue'

            task = Task(
                title=title,
                description=f'Detailed description for: {title}. This task requires careful attention and timely delivery.',
                employee_id=emp.id,
                priority=priority,
                status=status,
                due_date=due_date,
                progress=progress,
                quality_score=quality_score,
                created_at=created_at,
                completed_at=completed_at
            )
            db.session.add(task)

    db.session.flush()


def seed_attendance(employees):
    """Create attendance records for past 6 months."""
    today = date.today()
    start_date = today - timedelta(days=180)

    attendance_options = ['Present'] * 18 + ['Late'] * 2 + ['Leave'] * 2 + ['Absent'] * 1

    current_date = start_date
    while current_date <= today:
        # Skip weekends
        if current_date.weekday() < 5:
            for emp in employees:
                status = random.choice(attendance_options)
                check_in = None
                check_out = None

                if status == 'Present':
                    h = random.randint(8, 9)
                    m = random.randint(0, 55)
                    check_in = f'{h:02d}:{m:02d}'
                    h_out = random.randint(17, 19)
                    m_out = random.randint(0, 55)
                    check_out = f'{h_out:02d}:{m_out:02d}'
                elif status == 'Late':
                    h = random.randint(10, 11)
                    m = random.randint(0, 55)
                    check_in = f'{h:02d}:{m:02d}'
                    h_out = random.randint(18, 20)
                    m_out = random.randint(0, 55)
                    check_out = f'{h_out:02d}:{m_out:02d}'

                att = Attendance(
                    employee_id=emp.id,
                    date=current_date,
                    status=status,
                    check_in=check_in,
                    check_out=check_out
                )
                db.session.add(att)

        current_date += timedelta(days=1)

    db.session.flush()


def seed_performance(employees):
    """Create performance records for past 6 months."""
    today = date.today()

    for month_offset in range(6):
        period_date = today - timedelta(days=30 * month_offset)
        period = period_date.strftime('%Y-%m')

        for emp in employees:
            # Generate realistic scores with some variation
            base = random.uniform(65, 98)
            task_completion = round(min(100, max(40, base + random.uniform(-10, 10))), 1)
            quality = round(min(100, max(50, base + random.uniform(-8, 12))), 1)
            attendance = round(min(100, max(60, base + random.uniform(-5, 8))), 1)
            productivity = round(min(100, max(45, base + random.uniform(-12, 10))), 1)
            manager_rating = round(min(100, max(55, base + random.uniform(-8, 10))), 1)

            final_score, classification = calculate_performance_score(
                task_completion, quality, attendance, productivity, manager_rating
            )

            perf = Performance(
                employee_id=emp.id,
                period=period,
                task_completion=task_completion,
                quality_score=quality,
                attendance_score=attendance,
                productivity_score=productivity,
                manager_rating=manager_rating,
                final_score=final_score,
                classification=classification
            )
            db.session.add(perf)

    db.session.flush()


def seed_feedback(employees):
    """Create feedback records."""
    for emp in employees:
        num_feedback = random.randint(1, 3)
        for _ in range(num_feedback):
            fb_type = random.choice(['Appreciation', 'Improvement', 'General'])
            content = random.choice(FEEDBACK_TEMPLATES[fb_type])

            # Feedback given by a random other employee
            givers = [e for e in employees if e.id != emp.id]
            giver = random.choice(givers) if givers else None

            fb = Feedback(
                employee_id=emp.id,
                given_by=giver.id if giver else None,
                type=fb_type,
                content=content,
                created_at=datetime.now() - timedelta(days=random.randint(1, 90))
            )
            db.session.add(fb)

    db.session.flush()


def set_department_heads(departments, employees):
    """Set department heads."""
    dept_first_emp = {}
    for emp in employees:
        if emp.department_id not in dept_first_emp:
            dept_first_emp[emp.department_id] = emp

    for code, dept in departments.items():
        if dept.id in dept_first_emp:
            dept.head_id = dept_first_emp[dept.id].id

    db.session.flush()


def reset_data():
    """Clear all data and reseed."""
    Feedback.query.delete()
    Performance.query.delete()
    Attendance.query.delete()
    Task.query.delete()
    User.query.delete()
    Employee.query.delete()
    Department.query.delete()
    db.session.commit()
    seed_all()


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        db.create_all()
        reset_data()
        print("Database seeded successfully!")
