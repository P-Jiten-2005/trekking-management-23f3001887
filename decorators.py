from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'danger')
                return redirect(url_for('auth.login'))
            if current_user.is_blacklisted:
                flash('Your account has been blacklisted.', 'danger')
                # Redirect to logout so their session is cleared
                return redirect(url_for('auth.logout'))
            if not current_user.is_approved:
                # Redirect staff who aren't approved yet to the pending page
                return redirect(url_for('auth.pending_approval'))
            if current_user.role not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
