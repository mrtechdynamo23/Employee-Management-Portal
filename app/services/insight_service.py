"""
Automated Performance Insight generation.
Rule-based insights derived from workforce data.
"""
from app import db
from app.models.employee import Employee
from app.models.task import Task
from app.models.performance import Performance
from app.models.attendance import Attendance
from sqlalchemy import func
from datetime import datetime, timedelta


def generate_insights():
    """Generate automated performance insights from current data."""
    insights = []

    # 1. Top performer insight
    top = _get_top_performer_insight()
    if top:
        insights.append(top)

    # 2. Productivity trend
    prod = _get_productivity_trend_insight()
    if prod:
        insights.append(prod)

    # 3. Low performers warning
    low = _get_low_performers_insight()
    if low:
        insights.append(low)

    # 4. Deadline risk
    deadline = _get_deadline_risk_insight()
    if deadline:
        insights.append(deadline)

    # 5. Attendance insight
    att = _get_attendance_insight()
    if att:
        insights.append(att)

    # 6. Task completion insight
    tc = _get_task_completion_insight()
    if tc:
        insights.append(tc)

    # 7. Department performance
    dept = _get_department_insight()
    if dept:
        insights.append(dept)

    # 8. Overdue tasks
    overdue = _get_overdue_insight()
    if overdue:
        insights.append(overdue)

    return insights


def _get_top_performer_insight():
    """Identify the top performing employee."""
    latest_period = db.session.query(func.max(Performance.period)).scalar()
    if not latest_period:
        return None

    top = Performance.query.filter_by(period=latest_period).join(Employee).filter(
        Employee.status == 'Active'
    ).order_by(Performance.final_score.desc()).first()

    if top and top.employee:
        return {
            'type': 'top_performer',
            'icon': 'bi-trophy-fill',
            'color': '#F59E0B',
            'title': 'Top Performer',
            'message': f'{top.employee.full_name} currently leads the organization with a {top.final_score}% performance score.',
            'badge': 'warning'
        }
    return None


def _get_productivity_trend_insight():
    """Compare recent productivity with previous period."""
    periods = db.session.query(Performance.period).distinct().order_by(Performance.period.desc()).limit(2).all()
    if len(periods) < 2:
        return None

    current = db.session.query(func.avg(Performance.productivity_score)).filter(
        Performance.period == periods[0][0]
    ).scalar() or 0

    previous = db.session.query(func.avg(Performance.productivity_score)).filter(
        Performance.period == periods[1][0]
    ).scalar() or 0

    diff = round(current - previous, 1)
    if diff > 0:
        return {
            'type': 'positive',
            'icon': 'bi-graph-up-arrow',
            'color': '#10B981',
            'title': 'Productivity Rising',
            'message': f'Employee productivity increased by {abs(diff)}% compared with the previous period.',
            'badge': 'success'
        }
    elif diff < -2:
        return {
            'type': 'warning',
            'icon': 'bi-graph-down-arrow',
            'color': '#F59E0B',
            'title': 'Productivity Declining',
            'message': f'Employee productivity decreased by {abs(diff)}% compared with the previous period.',
            'badge': 'warning'
        }
    return None


def _get_low_performers_insight():
    """Count employees below performance threshold."""
    latest_period = db.session.query(func.max(Performance.period)).scalar()
    if not latest_period:
        return None

    count = Performance.query.filter(
        Performance.period == latest_period,
        Performance.task_completion < 70
    ).join(Employee).filter(Employee.status == 'Active').count()

    if count > 0:
        return {
            'type': 'warning',
            'icon': 'bi-exclamation-triangle-fill',
            'color': '#F59E0B',
            'title': 'Performance Alert',
            'message': f'{count} employee{"s" if count > 1 else ""} currently {"have" if count > 1 else "has"} task completion rates below the expected threshold.',
            'badge': 'warning'
        }
    return None


def _get_deadline_risk_insight():
    """Count tasks approaching deadlines."""
    deadline = datetime.utcnow().date() + timedelta(days=2)
    today = datetime.utcnow().date()
    count = Task.query.filter(
        Task.status != 'Completed',
        Task.due_date <= deadline,
        Task.due_date >= today
    ).count()

    if count > 0:
        return {
            'type': 'deadline',
            'icon': 'bi-alarm-fill',
            'color': '#EF4444',
            'title': 'Deadline Risk',
            'message': f'{count} task{"s are" if count > 1 else " is"} approaching {"their" if count > 1 else "its"} deadline{"s" if count > 1 else ""} within the next 48 hours.',
            'badge': 'danger'
        }
    return None


def _get_attendance_insight():
    """Get attendance rate insight."""
    today = datetime.utcnow().date()
    month_start = today.replace(day=1)
    total = Attendance.query.filter(Attendance.date >= month_start).count()
    present = Attendance.query.filter(
        Attendance.date >= month_start,
        Attendance.status.in_(['Present', 'Late'])
    ).count()

    if total > 0:
        rate = round((present / total) * 100, 1)
        if rate >= 95:
            return {
                'type': 'positive',
                'icon': 'bi-calendar-check-fill',
                'color': '#10B981',
                'title': 'Excellent Attendance',
                'message': f'Current month attendance rate is {rate}%, exceeding the organizational target.',
                'badge': 'success'
            }
        elif rate < 85:
            return {
                'type': 'warning',
                'icon': 'bi-calendar-x-fill',
                'color': '#F59E0B',
                'title': 'Attendance Concern',
                'message': f'Current month attendance rate is {rate}%, which is below the organizational target.',
                'badge': 'warning'
            }
    return None


def _get_task_completion_insight():
    """Get overall task completion insight."""
    total = Task.query.count()
    completed = Task.query.filter_by(status='Completed').count()
    if total > 0:
        rate = round((completed / total) * 100, 1)
        return {
            'type': 'info',
            'icon': 'bi-check-circle-fill',
            'color': '#6366F1',
            'title': 'Task Completion',
            'message': f'{completed} of {total} tasks have been completed ({rate}% completion rate).',
            'badge': 'primary'
        }
    return None


def _get_department_insight():
    """Find the best performing department."""
    from app.models.department import Department

    best_dept = None
    best_score = 0

    departments = Department.query.all()
    for dept in departments:
        avg = dept.avg_performance
        if avg > best_score:
            best_score = avg
            best_dept = dept

    if best_dept and best_score > 0:
        return {
            'type': 'positive',
            'icon': 'bi-building-fill',
            'color': '#10B981',
            'title': 'Department Leader',
            'message': f'{best_dept.name} leads all departments with an average performance score of {best_score}%.',
            'badge': 'success'
        }
    return None


def _get_overdue_insight():
    """Count overdue tasks."""
    count = Task.query.filter(
        Task.status != 'Completed',
        Task.due_date < datetime.utcnow().date()
    ).count()

    if count > 0:
        return {
            'type': 'danger',
            'icon': 'bi-clock-history',
            'color': '#EF4444',
            'title': 'Overdue Tasks',
            'message': f'{count} task{"s are" if count > 1 else " is"} currently overdue and {"require" if count > 1 else "requires"} immediate attention.',
            'badge': 'danger'
        }
    return None
