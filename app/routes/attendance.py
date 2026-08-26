"""Attendance tracking routes."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.attendance import Attendance
from app.models.employee import Employee
from app.models.department import Department
from datetime import date, datetime, timedelta
from sqlalchemy import func, case

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/')
@login_required
def index():
    """Attendance overview page."""
    today = date.today()

    # EMPLOYEE VIEW: Personal Attendance
    if not current_user.is_admin:
        emp = current_user.employee or Employee.query.filter_by(email=current_user.email).first()
        records = emp.attendances.order_by(Attendance.date.desc()).all() if emp else []
        
        total = len(records)
        present = sum(1 for r in records if r.status in ['Present', 'Late'])
        absent = sum(1 for r in records if r.status == 'Absent')
        leave = sum(1 for r in records if r.status == 'Leave')
        late = sum(1 for r in records if r.status == 'Late')
        
        today_att = emp.attendances.filter_by(date=today).first() if emp else None

        return render_template('employee_attendance.html',
                             employee=emp,
                             records=records,
                             total=total,
                             present=present,
                             absent=absent,
                             leave=leave,
                             late=late,
                             today_att=today_att)

    # ADMIN VIEW: Company Attendance
    selected_date = request.args.get('date', today.isoformat())
    dept_filter = request.args.get('department', '')
    view = request.args.get('view', 'daily')

    if view == 'daily':
        query = Attendance.query.filter_by(date=selected_date).join(Employee).filter(Employee.status == 'Active')
        if dept_filter:
            query = query.filter(Employee.department_id == dept_filter)
        records = query.order_by(Employee.first_name).all()

        total = len(records)
        present = sum(1 for r in records if r.status in ['Present', 'Late'])
        absent = sum(1 for r in records if r.status == 'Absent')
        leave = sum(1 for r in records if r.status == 'Leave')
        late = sum(1 for r in records if r.status == 'Late')
    else:
        records = []
        total = present = absent = leave = late = 0

    departments = Department.query.order_by(Department.name).all()

    month_start = today.replace(day=1)
    monthly_data = db.session.query(
        Attendance.date,
        func.count(Attendance.id).label('total'),
        func.sum(case((Attendance.status == 'Present', 1), else_=0)).label('present'),
        func.sum(case((Attendance.status == 'Absent', 1), else_=0)).label('absent'),
        func.sum(case((Attendance.status == 'Leave', 1), else_=0)).label('leave_count'),
        func.sum(case((Attendance.status == 'Late', 1), else_=0)).label('late')
    ).filter(Attendance.date >= month_start).group_by(Attendance.date).order_by(Attendance.date).all()

    return render_template('attendance.html',
                         records=records,
                         departments=departments,
                         selected_date=selected_date,
                         dept_filter=dept_filter,
                         view=view,
                         total=total,
                         present=present,
                         absent=absent,
                         leave=leave,
                         late=late,
                         monthly_data=monthly_data)


@attendance_bp.route('/check-in', methods=['POST'])
@login_required
def check_in():
    """Employee self punch-in."""
    emp = current_user.employee or Employee.query.filter_by(email=current_user.email).first()
    if not emp:
        flash('No employee profile linked to your account.', 'danger')
        return redirect(url_for('dashboard.index'))

    today = date.today()
    now_time = datetime.now().strftime('%I:%M %p')

    existing = Attendance.query.filter_by(employee_id=emp.id, date=today).first()
    if existing:
        flash('You have already punched in for today!', 'info')
    else:
        # If past 9:30 AM, mark as Late, else Present
        status = 'Late' if datetime.now().hour >= 10 or (datetime.now().hour == 9 and datetime.now().minute > 30) else 'Present'
        att = Attendance(
            employee_id=emp.id,
            date=today,
            status=status,
            check_in=now_time
        )
        db.session.add(att)
        db.session.commit()
        flash(f'Successfully punched in at {now_time} ({status})!', 'success')

    return redirect(request.referrer or url_for('dashboard.index'))


@attendance_bp.route('/mark', methods=['POST'])
@login_required
def mark():
    """Mark attendance for an employee."""
    employee_id = request.form.get('employee_id')
    att_date_raw = request.form.get('date')
    if att_date_raw:
        if isinstance(att_date_raw, date):
            att_date = att_date_raw
        else:
            try:
                att_date = date.fromisoformat(att_date_raw.strip())
            except (ValueError, TypeError):
                att_date = date.today()
    else:
        att_date = date.today()

    status = request.form.get('status', 'Present')
    check_in = request.form.get('check_in', '')
    check_out = request.form.get('check_out', '')

    # Check if already marked
    existing = Attendance.query.filter_by(employee_id=employee_id, date=att_date).first()
    if existing:
        existing.status = status
        existing.check_in = check_in or existing.check_in
        existing.check_out = check_out or existing.check_out
        flash('Attendance record updated.', 'success')
    else:
        att = Attendance(
            employee_id=employee_id,
            date=att_date,
            status=status,
            check_in=check_in,
            check_out=check_out
        )
        db.session.add(att)
        flash('Attendance marked successfully.', 'success')

    db.session.commit()
    return redirect(url_for('attendance.index', date=att_date.isoformat()))


@attendance_bp.route('/bulk-mark', methods=['POST'])
@login_required
def bulk_mark():
    """Bulk mark attendance."""
    att_date_raw = request.form.get('date')
    if att_date_raw:
        if isinstance(att_date_raw, date):
            att_date = att_date_raw
        else:
            try:
                att_date = date.fromisoformat(att_date_raw.strip())
            except (ValueError, TypeError):
                att_date = date.today()
    else:
        att_date = date.today()

    employees = Employee.query.filter_by(status='Active').all()

    for emp in employees:
        status = request.form.get(f'status_{emp.id}', 'Present')
        existing = Attendance.query.filter_by(employee_id=emp.id, date=att_date).first()
        if existing:
            existing.status = status
        else:
            att = Attendance(employee_id=emp.id, date=att_date, status=status)
            db.session.add(att)

    db.session.commit()
    flash('Bulk attendance marked successfully.', 'success')
    return redirect(url_for('attendance.index', date=att_date.isoformat()))
