"""
Report generation service using ReportLab.
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime


def _get_styles():
    """Get custom styles for reports."""
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='ReportTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=6,
        textColor=colors.HexColor('#6366F1'),
        alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        name='ReportSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#6B7280'),
        alignment=TA_CENTER,
        spaceAfter=20
    ))
    styles.add(ParagraphStyle(
        name='SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#111827'),
        spaceBefore=16,
        spaceAfter=8
    ))
    return styles


def _get_table_style():
    """Get standard table styling."""
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366F1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ])


def generate_employee_report():
    """Generate Employee Performance Report PDF."""
    from app.models.employee import Employee
    from app.models.performance import Performance
    from sqlalchemy import func

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=30*mm, bottomMargin=20*mm)
    styles = _get_styles()
    elements = []

    # Header
    elements.append(Paragraph('EmployeeHub', styles['ReportTitle']))
    elements.append(Paragraph(f'Employee Performance Report — Generated {datetime.now().strftime("%B %d, %Y")}', styles['ReportSubtitle']))
    elements.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#E5E7EB')))
    elements.append(Spacer(1, 12))

    # Summary
    total = Employee.query.filter_by(status='Active').count()
    avg = db.session.query(func.avg(Performance.final_score)).scalar() or 0
    elements.append(Paragraph(f'Total Active Employees: {total} | Average Performance: {round(avg, 1)}%', styles['Normal']))
    elements.append(Spacer(1, 12))

    # Table
    elements.append(Paragraph('Employee Details', styles['SectionTitle']))
    data = [['Code', 'Name', 'Department', 'Designation', 'Performance', 'Classification']]

    employees = Employee.query.filter_by(status='Active').order_by(Employee.first_name).all()
    for emp in employees:
        perf = emp.latest_performance
        data.append([
            emp.employee_code,
            emp.full_name,
            emp.department.name if emp.department else 'N/A',
            emp.designation or 'N/A',
            f'{perf.final_score}%' if perf else 'N/A',
            perf.classification if perf else 'N/A'
        ])

    col_widths = [55, 100, 90, 85, 65, 80]
    table = Table(data, colWidths=col_widths)
    table.setStyle(_get_table_style())
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_department_report():
    """Generate Department Report PDF."""
    from app.models.department import Department
    from app.models.employee import Employee
    from app.models.task import Task

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=30*mm, bottomMargin=20*mm)
    styles = _get_styles()
    elements = []

    elements.append(Paragraph('EmployeeHub', styles['ReportTitle']))
    elements.append(Paragraph(f'Department Report — Generated {datetime.now().strftime("%B %d, %Y")}', styles['ReportSubtitle']))
    elements.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#E5E7EB')))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph('Department Overview', styles['SectionTitle']))
    data = [['Department', 'Employees', 'Avg Performance', 'Tasks', 'Completion Rate']]

    departments = Department.query.all()
    for dept in departments:
        emp_count = dept.employees.filter_by(status='Active').count()
        avg_perf = dept.avg_performance
        dept_tasks = Task.query.join(Employee).filter(Employee.department_id == dept.id).count()
        completed = Task.query.join(Employee).filter(Employee.department_id == dept.id, Task.status == 'Completed').count()
        completion = round((completed / dept_tasks) * 100, 1) if dept_tasks > 0 else 0

        data.append([dept.name, str(emp_count), f'{avg_perf}%', str(dept_tasks), f'{completion}%'])

    col_widths = [120, 70, 100, 60, 100]
    table = Table(data, colWidths=col_widths)
    table.setStyle(_get_table_style())
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_attendance_report():
    """Generate Attendance Report PDF."""
    from app.models.attendance import Attendance
    from app.models.employee import Employee
    from sqlalchemy import func

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=30*mm, bottomMargin=20*mm)
    styles = _get_styles()
    elements = []

    elements.append(Paragraph('EmployeeHub', styles['ReportTitle']))
    elements.append(Paragraph(f'Attendance Report — Generated {datetime.now().strftime("%B %d, %Y")}', styles['ReportSubtitle']))
    elements.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#E5E7EB')))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph('Employee Attendance Summary', styles['SectionTitle']))
    data = [['Employee', 'Department', 'Present', 'Absent', 'Leave', 'Late', 'Rate']]

    employees = Employee.query.filter_by(status='Active').order_by(Employee.first_name).all()
    for emp in employees:
        total = emp.attendances.count()
        present = emp.attendances.filter_by(status='Present').count()
        absent = emp.attendances.filter_by(status='Absent').count()
        leave = emp.attendances.filter_by(status='Leave').count()
        late = emp.attendances.filter_by(status='Late').count()
        rate = round(((present + late) / total) * 100, 1) if total > 0 else 0

        data.append([
            emp.full_name,
            emp.department.name if emp.department else 'N/A',
            str(present), str(absent), str(leave), str(late),
            f'{rate}%'
        ])

    col_widths = [95, 80, 50, 50, 45, 45, 50]
    table = Table(data, colWidths=col_widths)
    table.setStyle(_get_table_style())
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_task_report():
    """Generate Task Report PDF."""
    from app.models.task import Task

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=30*mm, bottomMargin=20*mm)
    styles = _get_styles()
    elements = []

    elements.append(Paragraph('EmployeeHub', styles['ReportTitle']))
    elements.append(Paragraph(f'Task Report — Generated {datetime.now().strftime("%B %d, %Y")}', styles['ReportSubtitle']))
    elements.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#E5E7EB')))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph('Task Summary', styles['SectionTitle']))
    data = [['Task', 'Employee', 'Priority', 'Status', 'Due Date', 'Progress']]

    tasks = Task.query.order_by(Task.due_date.desc()).limit(50).all()
    for task in tasks:
        data.append([
            Paragraph(task.title[:30], styles['Normal']),
            task.employee.full_name if task.employee else 'Unassigned',
            task.priority,
            task.status,
            task.due_date.strftime('%Y-%m-%d') if task.due_date else 'N/A',
            f'{task.progress}%'
        ])

    col_widths = [120, 80, 55, 70, 70, 50]
    table = Table(data, colWidths=col_widths)
    table.setStyle(_get_table_style())
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer


# Need db import
from app import db
