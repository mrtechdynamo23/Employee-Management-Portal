"""Task model."""
from app import db
from datetime import datetime, date


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    priority = db.Column(db.String(20), default='Medium')  # Low, Medium, High, Critical
    status = db.Column(db.String(20), default='To Do')  # To Do, In Progress, Under Review, Completed, Overdue
    due_date = db.Column(db.Date, nullable=True)
    progress = db.Column(db.Integer, default=0)  # 0-100
    quality_score = db.Column(db.Float, nullable=True)  # Score given after completion
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def is_overdue(self):
        if self.status == 'Completed':
            return False
        if self.due_date and self.due_date < date.today():
            return True
        return False

    @property
    def priority_color(self):
        colors = {
            'Low': '#10B981',
            'Medium': '#6366F1',
            'High': '#F59E0B',
            'Critical': '#EF4444'
        }
        return colors.get(self.priority, '#6366F1')

    @property
    def status_color(self):
        colors = {
            'To Do': '#6B7280',
            'In Progress': '#6366F1',
            'Under Review': '#F59E0B',
            'Completed': '#10B981',
            'Overdue': '#EF4444'
        }
        return colors.get(self.status, '#6B7280')

    @property
    def days_until_due(self):
        if not self.due_date:
            return None
        delta = self.due_date - date.today()
        return delta.days

    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'
