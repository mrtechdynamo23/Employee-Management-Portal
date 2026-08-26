"""Performance model."""
from app import db
from datetime import datetime


class Performance(db.Model):
    __tablename__ = 'performances'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    period = db.Column(db.String(7), nullable=False)  # YYYY-MM format
    task_completion = db.Column(db.Float, default=0)    # 0-100
    quality_score = db.Column(db.Float, default=0)      # 0-100
    attendance_score = db.Column(db.Float, default=0)   # 0-100
    productivity_score = db.Column(db.Float, default=0) # 0-100
    manager_rating = db.Column(db.Float, default=0)     # 0-100
    final_score = db.Column(db.Float, default=0)        # Calculated
    classification = db.Column(db.String(20), default='N/A')
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def classification_color(self):
        colors = {
            'Excellent': '#10B981',
            'Very Good': '#6366F1',
            'Good': '#3B82F6',
            'Average': '#F59E0B',
            'Needs Improvement': '#EF4444'
        }
        return colors.get(self.classification, '#6B7280')

    @property
    def classification_badge(self):
        badges = {
            'Excellent': 'success',
            'Very Good': 'primary',
            'Good': 'info',
            'Average': 'warning',
            'Needs Improvement': 'danger'
        }
        return badges.get(self.classification, 'secondary')

    def __repr__(self):
        return f'<Performance {self.employee_id} - {self.period}: {self.final_score}>'
