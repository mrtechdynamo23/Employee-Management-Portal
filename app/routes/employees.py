"""Employee management routes."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.employee import Employee
from app.models.department import Department
from app.models.task import Task
from app.models.performance import Performance
from app.models.attendance import Attendance
from app.models.feedback import Feedback
from app.utils.validators import validate_employee_form
from app.utils.helpers import admin_required, generate_employee_code, generate_avatar_color

employees_bp = Blueprint('employees', __name__)


@employees_bp.route('/')
@login_required
@admin_required
def index():
    """Employee list page."""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    dept_filter = request.args.get('department', '')
    status_filter = request.args.get('status', '')
    perf_filter = request.args.get('performance', '')

    query = Employee.query

    if search:
        query = query.filter(
            db.or_(
                Employee.first_name.ilike(f'%{search}%'),
                Employee.last_name.ilike(f'%{search}%'),
                Employee.employee_code.ilike(f'%{search}%'),
                Employee.email.ilike(f'%{search}%')
            )
        )

    if dept_filter:
        query = query.filter(Employee.department_id == dept_filter)

    if status_filter:
        query = query.filter(Employee.status == status_filter)

    employees = query.order_by(Employee.first_name).paginate(page=page, per_page=15, error_out=False)
    departments = Department.query.order_by(Department.name).all()

    return render_template('employees.html',
                         employees=employees,
                         departments=departments,
                         search=search,
                         dept_filter=dept_filter,
                         status_filter=status_filter,
                         perf_filter=perf_filter)


@employees_bp.route('/add', methods=['POST'])
@login_required
@admin_required
def add():
    """Add new employee."""
    errors = validate_employee_form(request.form)
    if errors:
        for error in errors:
            flash(error, 'danger')
        return redirect(url_for('employees.index'))

    # Check duplicate email
    if Employee.query.filter_by(email=request.form.get('email').strip().lower()).first():
        flash('An employee with this email already exists.', 'danger')
        return redirect(url_for('employees.index'))

    last = Employee.query.order_by(Employee.id.desc()).first()
    emp_code = generate_employee_code(last.id if last else 0)

    doj_raw = request.form.get('date_of_joining')
    doj_val = None
    if doj_raw:
        if isinstance(doj_raw, date):
            doj_val = doj_raw
        else:
            try:
                doj_val = date.fromisoformat(doj_raw.strip())
            except (ValueError, TypeError):
                doj_val = None

    employee = Employee(
        employee_code=emp_code,
        first_name=request.form.get('first_name').strip(),
        last_name=request.form.get('last_name').strip(),
        email=request.form.get('email').strip().lower(),
        phone=request.form.get('phone', '').strip(),
        department_id=request.form.get('department_id') or None,
        designation=request.form.get('designation', '').strip(),
        date_of_joining=doj_val,
        avatar_color=generate_avatar_color()
    )
    db.session.add(employee)
    db.session.commit()
    flash(f'Employee {employee.full_name} added successfully.', 'success')
    return redirect(url_for('employees.index'))


@employees_bp.route('/<int:id>')
@login_required
def detail(id):
    """Employee detail/profile page."""
    # Allow admins, or employees viewing their own profile
    if not current_user.is_admin:
        emp = current_user.employee or Employee.query.filter_by(email=current_user.email).first()
        if not emp or emp.id != id:
            flash('Access restricted to your own profile.', 'warning')
            return redirect(url_for('dashboard.index'))

    employee = Employee.query.get_or_404(id)
    tasks = employee.tasks.order_by(Task.due_date.desc()).all()
    performances = employee.performances.order_by(Performance.period.desc()).all()
    attendances = employee.attendances.order_by(Attendance.date.desc()).limit(30).all()
    feedback_list = employee.feedback_received.order_by(Feedback.created_at.desc()).all()

    # Attendance stats
    total_att = employee.attendances.count()
    present = employee.attendances.filter(Attendance.status.in_(['Present', 'Late'])).count()
    attendance_rate = round((present / total_att) * 100, 1) if total_att > 0 else 0

    # Task stats
    total_tasks = employee.tasks.count()
    completed_tasks = employee.tasks.filter_by(status='Completed').count()

    return render_template('employee_details.html',
                         employee=employee,
                         tasks=tasks,
                         performances=performances,
                         attendances=attendances,
                         feedback_list=feedback_list,
                         attendance_rate=attendance_rate,
                         total_tasks=total_tasks,
                         completed_tasks=completed_tasks)


@employees_bp.route('/<int:id>/edit', methods=['POST'])
@login_required
@admin_required
def edit(id):
    """Update employee."""
    employee = Employee.query.get_or_404(id)

    errors = validate_employee_form(request.form)
    if errors:
        for error in errors:
            flash(error, 'danger')
        return redirect(url_for('employees.detail', id=id))

    # Check duplicate email (excluding current)
    existing = Employee.query.filter(Employee.email == request.form.get('email').strip().lower(),
                                      Employee.id != id).first()
    if existing:
        flash('An employee with this email already exists.', 'danger')
        return redirect(url_for('employees.detail', id=id))

    doj_raw = request.form.get('date_of_joining')
    if doj_raw:
        if isinstance(doj_raw, date):
            employee.date_of_joining = doj_raw
        else:
            try:
                employee.date_of_joining = date.fromisoformat(doj_raw.strip())
            except (ValueError, TypeError):
                pass

    employee.first_name = request.form.get('first_name').strip()
    employee.last_name = request.form.get('last_name').strip()
    employee.email = request.form.get('email').strip().lower()
    employee.phone = request.form.get('phone', '').strip()
    employee.department_id = request.form.get('department_id') or None
    employee.designation = request.form.get('designation', '').strip()

    db.session.commit()
    flash(f'Employee {employee.full_name} updated successfully.', 'success')
    return redirect(url_for('employees.detail', id=id))


@employees_bp.route('/<int:id>/deactivate', methods=['POST'])
@login_required
@admin_required
def deactivate(id):
    """Deactivate/activate employee."""
    employee = Employee.query.get_or_404(id)
    employee.status = 'Inactive' if employee.status == 'Active' else 'Active'
    db.session.commit()
    action = 'deactivated' if employee.status == 'Inactive' else 'activated'
    flash(f'Employee {employee.full_name} has been {action}.', 'success')
    return redirect(url_for('employees.index'))


@employees_bp.route('/search')
@login_required
def search_api():
    """API endpoint for employee search."""
    q = request.args.get('q', '')
    if len(q) < 2:
        return jsonify([])

    employees = Employee.query.filter(
        db.or_(
            Employee.first_name.ilike(f'%{q}%'),
            Employee.last_name.ilike(f'%{q}%'),
            Employee.employee_code.ilike(f'%{q}%')
        )
    ).filter_by(status='Active').limit(10).all()

    return jsonify([{
        'id': e.id,
        'name': e.full_name,
        'code': e.employee_code,
        'department': e.department.name if e.department else 'N/A'
    } for e in employees])
