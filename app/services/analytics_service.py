"""
Analytics service for aggregating workforce data.
"""
from app import db
from app.models.employee import Employee
from app.models.task import Task
from app.models.performance import Performance
from app.models.attendance import Attendance
from app.models.department import Department
from sqlalchemy import func, case
from datetime import datetime, timedelta


def get_dashboard_stats():
    """Get key performance indicators for the dashboard."""
    total_employees = Employee.query.filter_by(status='Active').count()
    total_all_employees = Employee.query.count()
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter_by(status='Completed').count()
    overdue_tasks = Task.query.filter(
        Task.status != 'Completed',
        Task.due_date < datetime.utcnow().date()
    ).count()

    completion_rate = round((completed_tasks / total_tasks) * 100, 1) if total_tasks > 0 else 0

    avg_performance = db.session.query(func.avg(Performance.final_score)).scalar()
    avg_performance = round(avg_performance, 1) if avg_performance else 0

    # Attendance rate for current month
    today = datetime.utcnow().date()
    month_start = today.replace(day=1)
    total_attendance = Attendance.query.filter(Attendance.date >= month_start).count()
    present_attendance = Attendance.query.filter(
        Attendance.date >= month_start,
        Attendance.status.in_(['Present', 'Late'])
    ).count()
    attendance_rate = round((present_attendance / total_attendance) * 100, 1) if total_attendance > 0 else 0

    return {
        'total_employees': total_employees,
        'total_all_employees': total_all_employees,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'completion_rate': completion_rate,
        'avg_performance': avg_performance,
        'attendance_rate': attendance_rate,
        'in_progress_tasks': Task.query.filter_by(status='In Progress').count(),
        'pending_tasks': Task.query.filter_by(status='To Do').count(),
    }


def get_performance_trend(months=6):
    """Get monthly average performance scores."""
    results = db.session.query(
        Performance.period,
        func.avg(Performance.final_score).label('avg_score')
    ).group_by(Performance.period).order_by(Performance.period.desc()).limit(months).all()

    results = list(reversed(results))
    return {
        'labels': [r.period for r in results],
        'data': [round(r.avg_score, 1) for r in results]
    }


def get_task_distribution():
    """Get task count by status."""
    results = db.session.query(
        Task.status,
        func.count(Task.id).label('count')
    ).group_by(Task.status).all()

    return {
        'labels': [r.status for r in results],
        'data': [r.count for r in results]
    }


def get_task_priority_distribution():
    """Get task count by priority."""
    results = db.session.query(
        Task.priority,
        func.count(Task.id).label('count')
    ).group_by(Task.priority).all()

    return {
        'labels': [r.priority for r in results],
        'data': [r.count for r in results]
    }


def get_department_performance():
    """Get average performance by department."""
    results = db.session.query(
        Department.name,
        func.avg(Performance.final_score).label('avg_score'),
        func.count(Employee.id).label('emp_count')
    ).join(Employee, Employee.department_id == Department.id
    ).join(Performance, Performance.employee_id == Employee.id
    ).group_by(Department.name).all()

    return {
        'labels': [r.name for r in results],
        'data': [round(r.avg_score, 1) for r in results],
        'counts': [r.emp_count for r in results]
    }


def get_attendance_trend(months=6):
    """Get monthly attendance rates."""
    results = db.session.query(
        func.strftime('%Y-%m', Attendance.date).label('month'),
        func.count(Attendance.id).label('total'),
        func.sum(case(
            (Attendance.status.in_(['Present', 'Late']), 1),
            else_=0
        )).label('present')
    ).group_by('month').order_by(func.strftime('%Y-%m', Attendance.date).desc()).limit(months).all()

    results = list(reversed(results))
    return {
        'labels': [r.month for r in results],
        'data': [round((r.present / r.total) * 100, 1) if r.total > 0 else 0 for r in results]
    }


def get_productivity_trend(months=6):
    """Get monthly productivity scores."""
    results = db.session.query(
        Performance.period,
        func.avg(Performance.productivity_score).label('avg_productivity')
    ).group_by(Performance.period).order_by(Performance.period.desc()).limit(months).all()

    results = list(reversed(results))
    return {
        'labels': [r.period for r in results],
        'data': [round(r.avg_productivity, 1) for r in results]
    }


def get_top_performers(limit=10):
    """Get top performing employees."""
    from sqlalchemy.orm import joinedload

    # Get the latest performance period
    latest_period = db.session.query(func.max(Performance.period)).scalar()
    if not latest_period:
        return []

    results = db.session.query(Performance).filter(
        Performance.period == latest_period
    ).join(Employee).filter(
        Employee.status == 'Active'
    ).order_by(Performance.final_score.desc()).limit(limit).all()

    return results


def get_department_stats():
    """Get detailed stats for each department."""
    departments = Department.query.all()
    stats = []
    for dept in departments:
        emp_count = dept.employees.filter_by(status='Active').count()
        avg_perf = dept.avg_performance

        # Task stats for department
        dept_tasks = Task.query.join(Employee).filter(Employee.department_id == dept.id).count()
        completed = Task.query.join(Employee).filter(
            Employee.department_id == dept.id,
            Task.status == 'Completed'
        ).count()
        task_completion = round((completed / dept_tasks) * 100, 1) if dept_tasks > 0 else 0

        stats.append({
            'department': dept,
            'employee_count': emp_count,
            'avg_performance': avg_perf,
            'total_tasks': dept_tasks,
            'task_completion': task_completion
        })

    return stats
