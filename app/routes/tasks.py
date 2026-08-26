"""Task management routes."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.task import Task
from app.models.employee import Employee
from app.utils.validators import validate_task_form
from datetime import datetime, date

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/')
@login_required
def index():
    """Task list / Kanban board page."""
    view = request.args.get('view', 'kanban')
    search = request.args.get('search', '')
    priority_filter = request.args.get('priority', '')
    status_filter = request.args.get('status', '')
    employee_filter = request.args.get('employee', '')

    query = Task.query

    # Scoping for employee vs admin
    if not current_user.is_admin:
        emp = current_user.employee or Employee.query.filter_by(email=current_user.email).first()
        if emp:
            query = query.filter(Task.employee_id == emp.id)
    elif employee_filter:
        query = query.filter(Task.employee_id == employee_filter)

    if search:
        query = query.filter(Task.title.ilike(f'%{search}%'))

    if priority_filter:
        query = query.filter(Task.priority == priority_filter)

    if status_filter:
        query = query.filter(Task.status == status_filter)

    # Update overdue status
    overdue = Task.query.filter(
        Task.status.notin_(['Completed', 'Overdue']),
        Task.due_date < date.today()
    ).all()
    for t in overdue:
        t.status = 'Overdue'
    if overdue:
        db.session.commit()

    tasks = query.order_by(Task.due_date.asc()).all()
    employees = Employee.query.filter_by(status='Active').order_by(Employee.first_name).all()

    # Group tasks by status for Kanban
    kanban = {
        'To Do': [t for t in tasks if t.status == 'To Do'],
        'In Progress': [t for t in tasks if t.status == 'In Progress'],
        'Under Review': [t for t in tasks if t.status == 'Under Review'],
        'Completed': [t for t in tasks if t.status == 'Completed'],
        'Overdue': [t for t in tasks if t.status == 'Overdue'],
    }

    return render_template('tasks.html',
                         tasks=tasks,
                         kanban=kanban,
                         employees=employees,
                         view=view,
                         search=search,
                         priority_filter=priority_filter,
                         status_filter=status_filter,
                         employee_filter=employee_filter)


@tasks_bp.route('/add', methods=['POST'])
@login_required
def add():
    """Add new task."""
    if not current_user.is_admin:
        flash('Only administrators can assign new tasks.', 'warning')
        return redirect(url_for('tasks.index'))

    errors = validate_task_form(request.form)
    if errors:
        for error in errors:
            flash(error, 'danger')
        return redirect(url_for('tasks.index'))

    due_date_raw = request.form.get('due_date')
    due_date_val = None
    if due_date_raw:
        if isinstance(due_date_raw, date):
            due_date_val = due_date_raw
        else:
            try:
                due_date_val = date.fromisoformat(due_date_raw.strip())
            except (ValueError, TypeError):
                due_date_val = None

    task = Task(
        title=request.form.get('title').strip(),
        description=request.form.get('description', '').strip(),
        employee_id=request.form.get('employee_id') or None,
        priority=request.form.get('priority', 'Medium'),
        status='To Do',
        due_date=due_date_val,
        progress=0
    )
    db.session.add(task)
    db.session.commit()
    flash(f'Task "{task.title}" created successfully.', 'success')
    return redirect(url_for('tasks.index'))


@tasks_bp.route('/<int:id>/update', methods=['POST'])
@login_required
def update(id):
    """Update task."""
    task = Task.query.get_or_404(id)

    # If employee, ensure task is assigned to them
    if not current_user.is_admin:
        emp = current_user.employee or Employee.query.filter_by(email=current_user.email).first()
        if not emp or task.employee_id != emp.id:
            flash('You do not have permission to modify this task.', 'danger')
            return redirect(url_for('tasks.index'))

    if current_user.is_admin:
        task.title = request.form.get('title', task.title).strip()
        task.description = request.form.get('description', task.description)
        task.employee_id = request.form.get('employee_id') or task.employee_id
        task.priority = request.form.get('priority', task.priority)
        due_date_raw = request.form.get('due_date')
        if due_date_raw:
            if isinstance(due_date_raw, date):
                task.due_date = due_date_raw
            else:
                try:
                    task.due_date = date.fromisoformat(due_date_raw.strip())
                except (ValueError, TypeError):
                    pass

    task.progress = int(request.form.get('progress', task.progress))

    new_status = request.form.get('status', task.status)
    if new_status == 'Completed' and task.status != 'Completed':
        task.completed_at = datetime.utcnow()
        task.progress = 100
        if current_user.is_admin:
            task.quality_score = float(request.form.get('quality_score', 85))
    task.status = new_status

    db.session.commit()
    flash(f'Task "{task.title}" updated successfully.', 'success')
    return redirect(url_for('tasks.index'))


@tasks_bp.route('/<int:id>/status', methods=['POST'])
@login_required
def update_status(id):
    """Update task status (for Kanban drag-drop)."""
    task = Task.query.get_or_404(id)

    # Permission check for employee
    if not current_user.is_admin:
        emp = current_user.employee or Employee.query.filter_by(email=current_user.email).first()
        if not emp or task.employee_id != emp.id:
            return jsonify({'success': False, 'message': 'Permission denied'}), 403

    data = request.get_json()
    new_status = data.get('status')

    if new_status in ['To Do', 'In Progress', 'Under Review', 'Completed', 'Overdue']:
        if new_status == 'Completed' and task.status != 'Completed':
            task.completed_at = datetime.utcnow()
            task.progress = 100
            if not task.quality_score:
                task.quality_score = 85.0
        task.status = new_status
        db.session.commit()
        return jsonify({'success': True, 'message': f'Task moved to {new_status}'})

    return jsonify({'success': False, 'message': 'Invalid status'}), 400


@tasks_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Delete task."""
    if not current_user.is_admin:
        flash('Only administrators can delete tasks.', 'danger')
        return redirect(url_for('tasks.index'))

    task = Task.query.get_or_404(id)
    title = task.title
    db.session.delete(task)
    db.session.commit()
    flash(f'Task "{title}" deleted successfully.', 'success')
    return redirect(url_for('tasks.index'))
