"""Reports and CSV export routes."""
from flask import Blueprint, render_template, send_file, request
from flask_login import login_required
from app.services.report_service import (
    generate_employee_report, generate_department_report,
    generate_attendance_report, generate_task_report
)
from app.models.employee import Employee
from app.models.task import Task
from app.models.performance import Performance
from app.models.attendance import Attendance
from app.utils.helpers import admin_required
import pandas as pd
from io import BytesIO, StringIO

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/')
@login_required
@admin_required
def index():
    """Reports page."""
    return render_template('reports.html')


@reports_bp.route('/pdf/<report_type>')
@login_required
def download_pdf(report_type):
    """Download PDF report."""
    generators = {
        'employee': (generate_employee_report, 'Employee_Performance_Report.pdf'),
        'department': (generate_department_report, 'Department_Report.pdf'),
        'attendance': (generate_attendance_report, 'Attendance_Report.pdf'),
        'task': (generate_task_report, 'Task_Report.pdf'),
    }

    if report_type not in generators:
        return 'Invalid report type', 404

    generator, filename = generators[report_type]
    buffer = generator()

    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )


@reports_bp.route('/csv/<data_type>')
@login_required
def download_csv(data_type):
    """Download CSV export."""
    if data_type == 'employees':
        employees = Employee.query.filter_by(status='Active').all()
        data = [{
            'Employee Code': e.employee_code,
            'Name': e.full_name,
            'Email': e.email,
            'Phone': e.phone or '',
            'Department': e.department.name if e.department else '',
            'Designation': e.designation or '',
            'Date of Joining': str(e.date_of_joining) if e.date_of_joining else '',
            'Status': e.status,
            'Performance Score': e.latest_performance_score,
            'Task Completion Rate': e.task_completion_rate
        } for e in employees]
        filename = 'Employees_Export.csv'

    elif data_type == 'tasks':
        tasks = Task.query.all()
        data = [{
            'Task ID': t.id,
            'Title': t.title,
            'Employee': t.employee.full_name if t.employee else 'Unassigned',
            'Priority': t.priority,
            'Status': t.status,
            'Due Date': str(t.due_date) if t.due_date else '',
            'Progress': f'{t.progress}%',
            'Quality Score': t.quality_score or '',
            'Created': str(t.created_at.date()) if t.created_at else ''
        } for t in tasks]
        filename = 'Tasks_Export.csv'

    elif data_type == 'performance':
        perfs = Performance.query.join(Employee).order_by(Performance.period.desc()).all()
        data = [{
            'Employee': p.employee.full_name if p.employee else '',
            'Period': p.period,
            'Task Completion': p.task_completion,
            'Quality Score': p.quality_score,
            'Attendance Score': p.attendance_score,
            'Productivity Score': p.productivity_score,
            'Manager Rating': p.manager_rating,
            'Final Score': p.final_score,
            'Classification': p.classification
        } for p in perfs]
        filename = 'Performance_Export.csv'

    elif data_type == 'attendance':
        records = Attendance.query.join(Employee).order_by(Attendance.date.desc()).limit(5000).all()
        data = [{
            'Employee': a.employee.full_name if a.employee else '',
            'Date': str(a.date),
            'Status': a.status,
            'Check In': a.check_in or '',
            'Check Out': a.check_out or ''
        } for a in records]
        filename = 'Attendance_Export.csv'

    else:
        return 'Invalid data type', 404

    df = pd.DataFrame(data)
    buffer = BytesIO()
    df.to_csv(buffer, index=False, encoding='utf-8')
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='text/csv'
    )
