"""Performance tracking routes."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.employee import Employee
from app.models.performance import Performance
from app.models.department import Department
from app.services.performance_service import calculate_performance_score
from app.utils.validators import validate_performance_form

performance_bp = Blueprint('performance', __name__)


@performance_bp.route('/')
@login_required
def index():
    """Performance overview page — role-based."""
    # EMPLOYEE VIEW: Personal Performance Scorecard
    if not current_user.is_admin:
        emp = current_user.employee or Employee.query.filter_by(email=current_user.email).first()
        performances = emp.performances.order_by(Performance.period.desc()).all() if emp else []
        latest_perf = emp.latest_performance if emp else None
        
        return render_template('employee_performance.html',
                             employee=emp,
                             performances=performances,
                             latest_perf=latest_perf)

    # ADMIN VIEW: Company Performance Matrix
    dept_filter = request.args.get('department', '')
    class_filter = request.args.get('classification', '')
    search = request.args.get('search', '')

    from sqlalchemy import func
    latest_period = db.session.query(func.max(Performance.period)).scalar()

    query = Performance.query.filter_by(period=latest_period).join(Employee).filter(Employee.status == 'Active')

    if dept_filter:
        query = query.filter(Employee.department_id == dept_filter)

    if class_filter:
        query = query.filter(Performance.classification == class_filter)

    if search:
        query = query.filter(
            db.or_(
                Employee.first_name.ilike(f'%{search}%'),
                Employee.last_name.ilike(f'%{search}%')
            )
        )

    performances = query.order_by(Performance.final_score.desc()).all()
    departments = Department.query.order_by(Department.name).all()

    return render_template('performance.html',
                         performances=performances,
                         departments=departments,
                         latest_period=latest_period,
                         dept_filter=dept_filter,
                         class_filter=class_filter,
                         search=search)


@performance_bp.route('/add', methods=['POST'])
@login_required
def add():
    """Add performance record."""
    errors = validate_performance_form(request.form)
    if errors:
        for error in errors:
            flash(error, 'danger')
        return redirect(url_for('performance.index'))

    employee_id = request.form.get('employee_id')
    period = request.form.get('period')

    # Check if record already exists for this period
    existing = Performance.query.filter_by(employee_id=employee_id, period=period).first()
    if existing:
        flash('Performance record already exists for this employee and period.', 'warning')
        return redirect(url_for('performance.index'))

    tc = float(request.form.get('task_completion', 0))
    qs = float(request.form.get('quality_score', 0))
    ats = float(request.form.get('attendance_score', 0))
    ps = float(request.form.get('productivity_score', 0))
    mr = float(request.form.get('manager_rating', 0))

    final_score, classification = calculate_performance_score(tc, qs, ats, ps, mr)

    perf = Performance(
        employee_id=employee_id,
        period=period,
        task_completion=tc,
        quality_score=qs,
        attendance_score=ats,
        productivity_score=ps,
        manager_rating=mr,
        final_score=final_score,
        classification=classification,
        notes=request.form.get('notes', '')
    )
    db.session.add(perf)
    db.session.commit()
    flash(f'Performance record added. Score: {final_score}% ({classification})', 'success')
    return redirect(url_for('performance.index'))


@performance_bp.route('/leaderboard')
@login_required
def leaderboard():
    """Leaderboard page."""
    from app.services.analytics_service import get_top_performers
    top_performers = get_top_performers(10)
    return render_template('leaderboard.html', top_performers=top_performers)


@performance_bp.route('/calculate', methods=['POST'])
@login_required
def calculate():
    """API to calculate performance score."""
    data = request.get_json()
    tc = float(data.get('task_completion', 0))
    qs = float(data.get('quality_score', 0))
    ats = float(data.get('attendance_score', 0))
    ps = float(data.get('productivity_score', 0))
    mr = float(data.get('manager_rating', 0))

    final_score, classification = calculate_performance_score(tc, qs, ats, ps, mr)
    return jsonify({
        'final_score': final_score,
        'classification': classification
    })
