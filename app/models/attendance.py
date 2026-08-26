"""Attendance model."""
from app import db
from datetime import datetime


class Attendance(db.Model):
    __tablename__ = 'attendances'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='Present')  # Present, Absent, Leave, Late
    check_in = db.Column(db.String(10), nullable=True)   # HH:MM format
    check_out = db.Column(db.String(10), nullable=True)   # HH:MM format
    notes = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def status_color(self):
        colors = {
            'Present': '#10B981',
            'Absent': '#EF4444',
            'Leave': '#F59E0B',
            'Late': '#F97316'
        }
        return colors.get(self.status, '#6B7280')

    @property
    def status_icon(self):
        icons = {
            'Present': 'bi-check-circle-fill',
            'Absent': 'bi-x-circle-fill',
            'Leave': 'bi-calendar-x-fill',
            'Late': 'bi-clock-fill'
        }
        return icons.get(self.status, 'bi-circle')

    def __repr__(self):
        return f'<Attendance {self.employee_id} - {self.date}: {self.status}>'
