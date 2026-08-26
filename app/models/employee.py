"""Employee model."""
from app import db
from datetime import datetime


class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    employee_code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    designation = db.Column(db.String(100), nullable=True)
    date_of_joining = db.Column(db.Date, nullable=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    status = db.Column(db.String(20), default='Active')  # Active, Inactive
    avatar_color = db.Column(db.String(7), default='#6366F1')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    department = db.relationship('Department', backref=db.backref('employees', lazy='dynamic'), foreign_keys=[department_id])
    manager = db.relationship('Employee', remote_side=[id], backref=db.backref('direct_reports', lazy='dynamic'))
    tasks = db.relationship('Task', backref='employee', lazy='dynamic', foreign_keys='Task.employee_id')
    performances = db.relationship('Performance', backref='employee', lazy='dynamic')
    attendances = db.relationship('Attendance', backref='employee', lazy='dynamic')
    feedback_received = db.relationship('Feedback', backref='employee', lazy='dynamic', foreign_keys='Feedback.employee_id')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def initials(self):
        return f'{self.first_name[0]}{self.last_name[0]}'

    @property
    def task_completion_rate(self):
        total = self.tasks.count()
        if total == 0:
            return 0
        completed = self.tasks.filter_by(status='Completed').count()
        return round((completed / total) * 100, 1)

    @property
    def latest_performance(self):
        return self.performances.order_by(Performance.created_at.desc()).first()

    @property
    def latest_performance_score(self):
        perf = self.latest_performance
        return perf.final_score if perf else 0

    @property
    def latest_classification(self):
        perf = self.latest_performance
        return perf.classification if perf else 'N/A'

    def __repr__(self):
        return f'<Employee {self.employee_code}: {self.full_name}>'


# Import at bottom to avoid circular imports
from app.models.performance import Performance
