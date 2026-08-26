"""Dashboard routes."""
from flask import Blueprint, render_template, jsonify, redirect, url_for
from flask_login import login_required, current_user
from datetime import date, datetime
from app import db
from app.models.employee import Employee
from app.models.task import Task
from app.models.performance import Performance
from app.models.attendance import Attendance
from app.services.analytics_service import get_dashboard_stats, get_performance_trend, \
    get_task_distribution, get_department_performance, get_attendance_trend, \
    get_productivity_trend, get_top_performers
from app.services.insight_service import generate_insights

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def index():
    """Main dashboard — role-based routing."""
    # ADMIN VIEW
    if current_user.is_admin:
        stats = get_dashboard_stats()
        top_performers = get_top_performers(5)
        insights = generate_insights()

        return render_template('dashboard.html',
                             stats=stats,
                             top_performers=top_performers,
                             insights=insights)

    # EMPLOYEE VIEW: Personalized Workspace
    emp = current_user.employee or Employee.query.filter_by(email=current_user.email).first()
    if not emp:
        # Fallback if no linked employee profile
        return render_template('dashboard.html',
                             stats=get_dashboard_stats(),
                             top_performers=get_top_performers(5),
                             insights=generate_insights())

    # Personal Task Stats
    my_tasks = Task.query.filter_by(employee_id=emp.id)
    total_tasks = my_tasks.count()
    completed_tasks = my_tasks.filter_by(status='Completed').count()
    in_progress_tasks = my_tasks.filter_by(status='In Progress').count()
    todo_tasks = my_tasks.filter_by(status='To Do').count()
    overdue_tasks = my_tasks.filter(
        Task.status.notin_(['Completed']),
        Task.due_date < date.today()
    ).count()

    completion_rate = round((completed_tasks / total_tasks) * 100, 1) if total_tasks > 0 else 0
    active_tasks = my_tasks.filter(Task.status != 'Completed').order_by(Task.due_date.asc()).all()

    # Personal Performance
    latest_perf = emp.latest_performance
    perf_history = emp.performances.order_by(Performance.period.asc()).all()

    # Personal Attendance this month
    today = date.today()
    month_start = today.replace(day=1)
    month_attendances = emp.attendances.filter(Attendance.date >= month_start).all()
    month_total_days = len(month_attendances)
    month_present = sum(1 for a in month_attendances if a.status in ['Present', 'Late'])
    month_absent = sum(1 for a in month_attendances if a.status == 'Absent')
    month_leave = sum(1 for a in month_attendances if a.status == 'Leave')
    month_late = sum(1 for a in month_attendances if a.status == 'Late')
    attendance_rate = round((month_present / month_total_days) * 100, 1) if month_total_days > 0 else 100.0

    today_attendance = emp.attendances.filter_by(date=today).first()

    # Personal Feedback
    recent_feedback = emp.feedback_received.order_by(db.desc('created_at')).limit(5).all()

    # Leaderboard position
    all_top = get_top_performers(100)
    my_rank = None
    for idx, p in enumerate(all_top, 1):
        if p.employee_id == emp.id:
            my_rank = idx
            break

    return render_template('employee_dashboard.html',
                         employee=emp,
                         total_tasks=total_tasks,
                         completed_tasks=completed_tasks,
                         in_progress_tasks=in_progress_tasks,
                         todo_tasks=todo_tasks,
                         overdue_tasks=overdue_tasks,
                         completion_rate=completion_rate,
                         active_tasks=active_tasks,
                         latest_perf=latest_perf,
                         perf_history=perf_history,
                         month_present=month_present,
                         month_absent=month_absent,
                         month_leave=month_leave,
                         month_late=month_late,
                         attendance_rate=attendance_rate,
                         today_attendance=today_attendance,
                         recent_feedback=recent_feedback,
                         my_rank=my_rank)


@dashboard_bp.route('/dashboard/charts')
@login_required
def charts_data():
    """API endpoint for dashboard chart data."""
    perf_trend = get_performance_trend()
    task_dist = get_task_distribution()
    dept_perf = get_department_performance()
    att_trend = get_attendance_trend()
    prod_trend = get_productivity_trend()

    return jsonify({
        'performance_trend': perf_trend,
        'task_distribution': task_dist,
        'department_performance': dept_perf,
        'attendance_trend': att_trend,
        'productivity_trend': prod_trend
    })


@dashboard_bp.route('/settings')
@login_required
def settings():
    """Settings page."""
    return render_template('settings.html')
