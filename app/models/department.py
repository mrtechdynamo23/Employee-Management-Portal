"""Department model."""
from app import db
from datetime import datetime


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    head_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    head = db.relationship('Employee', foreign_keys=[head_id], backref=db.backref('headed_department', uselist=False))

    @property
    def employee_count(self):
        return self.employees.filter_by(status='Active').count()

    @property
    def avg_performance(self):
        from app.models.performance import Performance
        from sqlalchemy import func
        result = db.session.query(func.avg(Performance.final_score)).join(
            Employee, Performance.employee_id == Employee.id
        ).filter(Employee.department_id == self.id, Employee.status == 'Active').scalar()
        return round(result, 1) if result else 0

    def __repr__(self):
        return f'<Department {self.code}: {self.name}>'


from app.models.employee import Employee
