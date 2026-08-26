"""
Performance calculation service.
Implements the weighted performance scoring algorithm.
"""


def calculate_performance_score(task_completion, quality_score, attendance_score,
                                 productivity_score, manager_rating):
    """
    Calculate the final performance score using weighted metrics.

    Weights:
        - Task Completion: 30%
        - Task Quality: 25%
        - Attendance: 15%
        - Productivity: 20%
        - Manager Rating: 10%

    Args:
        task_completion (float): Task completion rate (0-100)
        quality_score (float): Quality of work score (0-100)
        attendance_score (float): Attendance percentage (0-100)
        productivity_score (float): Productivity metric (0-100)
        manager_rating (float): Manager's rating (0-100)

    Returns:
        tuple: (final_score, classification)
    """
    # Clamp all values between 0 and 100
    tc = max(0, min(100, float(task_completion or 0)))
    qs = max(0, min(100, float(quality_score or 0)))
    at = max(0, min(100, float(attendance_score or 0)))
    pr = max(0, min(100, float(productivity_score or 0)))
    mr = max(0, min(100, float(manager_rating or 0)))

    # Weighted calculation
    final_score = (
        tc * 0.30 +
        qs * 0.25 +
        at * 0.15 +
        pr * 0.20 +
        mr * 0.10
    )

    final_score = round(final_score, 1)

    # Classification
    classification = get_classification(final_score)

    return final_score, classification


def get_classification(score):
    """Get performance classification from score."""
    if score >= 90:
        return 'Excellent'
    elif score >= 80:
        return 'Very Good'
    elif score >= 70:
        return 'Good'
    elif score >= 60:
        return 'Average'
    else:
        return 'Needs Improvement'


def calculate_employee_task_metrics(employee):
    """Calculate task-based metrics for an employee."""
    from app.models.task import Task

    total_tasks = employee.tasks.count()
    if total_tasks == 0:
        return {'completion_rate': 0, 'avg_quality': 0, 'on_time_rate': 0}

    completed = employee.tasks.filter_by(status='Completed').count()
    completion_rate = round((completed / total_tasks) * 100, 1)

    # Average quality of completed tasks
    completed_tasks = employee.tasks.filter(
        Task.status == 'Completed',
        Task.quality_score.isnot(None)
    ).all()

    avg_quality = 0
    if completed_tasks:
        avg_quality = round(sum(t.quality_score for t in completed_tasks) / len(completed_tasks), 1)

    # On-time completion rate
    on_time = sum(1 for t in completed_tasks if t.completed_at and t.due_date and t.completed_at.date() <= t.due_date)
    on_time_rate = round((on_time / len(completed_tasks)) * 100, 1) if completed_tasks else 0

    return {
        'total_tasks': total_tasks,
        'completed': completed,
        'completion_rate': completion_rate,
        'avg_quality': avg_quality,
        'on_time_rate': on_time_rate
    }


def calculate_employee_attendance_score(employee_id, period=None):
    """Calculate attendance score for an employee."""
    from app.models.attendance import Attendance
    from sqlalchemy import func

    query = Attendance.query.filter_by(employee_id=employee_id)
    if period:
        query = query.filter(func.strftime('%Y-%m', Attendance.date) == period)

    total = query.count()
    if total == 0:
        return 0

    present = query.filter(Attendance.status.in_(['Present', 'Late'])).count()
    return round((present / total) * 100, 1)


def calculate_productivity_score(employee):
    """Calculate productivity score based on task progress and completion speed."""
    from app.models.task import Task

    tasks = employee.tasks.all()
    if not tasks:
        return 0

    scores = []
    for task in tasks:
        if task.status == 'Completed':
            scores.append(100)
        elif task.status == 'Overdue' or task.is_overdue:
            scores.append(max(0, task.progress - 20))
        elif task.status == 'In Progress':
            scores.append(task.progress)
        elif task.status == 'Under Review':
            scores.append(85)
        else:
            scores.append(task.progress * 0.5)

    return round(sum(scores) / len(scores), 1) if scores else 0
