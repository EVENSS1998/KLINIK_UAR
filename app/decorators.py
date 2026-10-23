from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Anda harus login terlebih dahulu', 'danger')
            return redirect(url_for('auth.login'))
        elif current_user.role != 'admin':
            flash('Anda tidak memiliki akses ke halaman ini', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated