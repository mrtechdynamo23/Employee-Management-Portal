"""Feedback model."""
from app import db
from datetime import datetime


class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    given_by = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    type = db.Column(db.String(20), default='General')  # Appreciation, Improvement, General
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    giver = db.relationship('Employee', foreign_keys=[given_by], backref=db.backref('feedback_given', lazy='dynamic'))

    @property
    def type_color(self):
        colors = {
            'Appreciation': '#10B981',
            'Improvement': '#F59E0B',
            'General': '#6366F1'
        }
        return colors.get(self.type, '#6B7280')

    @property
    def type_icon(self):
        icons = {
            'Appreciation': 'bi-star-fill',
            'Improvement': 'bi-arrow-up-circle-fill',
            'General': 'bi-chat-dots-fill'
        }
        return icons.get(self.type, 'bi-chat-dots')

    def __repr__(self):
        return f'<Feedback {self.id} for Employee {self.employee_id}>'
