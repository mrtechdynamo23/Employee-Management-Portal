"""Input validation utilities."""
import re


def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone):
    """Validate phone number format."""
    if not phone:
        return True
    pattern = r'^[\d\s\-\+\(\)]{7,15}$'
    return bool(re.match(pattern, phone))


def validate_required(value, field_name):
    """Check if a required field has a value."""
    if not value or (isinstance(value, str) and not value.strip()):
        return False, f'{field_name} is required.'
    return True, ''


def validate_employee_form(data):
    """Validate employee form data."""
    errors = []

    valid, msg = validate_required(data.get('first_name'), 'First name')
    if not valid:
        errors.append(msg)

    valid, msg = validate_required(data.get('last_name'), 'Last name')
    if not valid:
        errors.append(msg)

    valid, msg = validate_required(data.get('email'), 'Email')
    if not valid:
        errors.append(msg)
    elif not validate_email(data.get('email', '')):
        errors.append('Invalid email format.')

    if data.get('phone') and not validate_phone(data.get('phone')):
        errors.append('Invalid phone number format.')

    return errors


def validate_task_form(data):
    """Validate task form data."""
    errors = []

    valid, msg = validate_required(data.get('title'), 'Task title')
    if not valid:
        errors.append(msg)

    if data.get('priority') not in ['Low', 'Medium', 'High', 'Critical']:
        errors.append('Invalid priority level.')

    return errors


def validate_performance_form(data):
    """Validate performance form data."""
    errors = []

    for field in ['task_completion', 'quality_score', 'attendance_score', 'productivity_score', 'manager_rating']:
        try:
            val = float(data.get(field, 0))
            if val < 0 or val > 100:
                errors.append(f'{field.replace("_", " ").title()} must be between 0 and 100.')
        except (ValueError, TypeError):
            errors.append(f'{field.replace("_", " ").title()} must be a valid number.')

    return errors
