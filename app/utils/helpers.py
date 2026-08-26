"""Helper utilities."""
from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user
import random


def admin_required(f):
    """Decorator to restrict access to admin users."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def generate_employee_code(last_id):
    """Generate employee code like EMP001."""
    return f'EMP{str(last_id + 1).zfill(3)}'


def generate_avatar_color():
    """Generate a random avatar color from a predefined palette."""
    colors = [
        '#6366F1', '#8B5CF6', '#EC4899', '#EF4444', '#F59E0B',
        '#10B981', '#3B82F6', '#06B6D4', '#8B5CF6', '#F97316',
        '#14B8A6', '#6366F1', '#A855F7', '#D946EF', '#0EA5E9'
    ]
    return random.choice(colors)


def format_date(date_obj, fmt='%b %d, %Y'):
    """Format a date object to string."""
    if date_obj:
        return date_obj.strftime(fmt)
    return 'N/A'


def format_percentage(value):
    """Format a number as percentage."""
    if value is None:
        return '0%'
    return f'{round(value, 1)}%'


def get_month_name(period):
    """Convert YYYY-MM to month name."""
    from datetime import datetime
    try:
        dt = datetime.strptime(period, '%Y-%m')
        return dt.strftime('%b %Y')
    except (ValueError, TypeError):
        return period
