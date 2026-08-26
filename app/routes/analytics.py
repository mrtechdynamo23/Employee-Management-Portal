"""Analytics routes."""
from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from app.services.analytics_service import (
    get_performance_trend, get_task_distribution, get_task_priority_distribution,
    get_department_performance, get_attendance_trend, get_productivity_trend,
    get_department_stats, get_top_performers
)
from app.services.insight_service import generate_insights

from app.utils.helpers import admin_required

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/')
@login_required
@admin_required
def index():
    """Analytics dashboard page."""
    dept_stats = get_department_stats()
    insights = generate_insights()
    top_performers = get_top_performers(5)

    return render_template('analytics.html',
                         dept_stats=dept_stats,
                         insights=insights,
                         top_performers=top_performers)


@analytics_bp.route('/data')
@login_required
def data():
    """API endpoint for analytics chart data."""
    return jsonify({
        'performance_trend': get_performance_trend(),
        'task_distribution': get_task_distribution(),
        'task_priority': get_task_priority_distribution(),
        'department_performance': get_department_performance(),
        'attendance_trend': get_attendance_trend(),
        'productivity_trend': get_productivity_trend()
    })
