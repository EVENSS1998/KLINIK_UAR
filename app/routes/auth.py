from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import user

auth_valo = Blueprint('auth', __name__)

@auth_valo.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        pengguna = user.query.filter_by(username=username).first()
        if pengguna and pengguna.check_password(password):
            login_user(pengguna)
            return redirect(url_for('main.index'))
        else:
            flash('salah username atau password', 'danger')
    
    return render_template('auth/login.html')

@auth_valo.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = user.query.filter_by(username=username).first()
        if user:
            flash('username sudah ada', 'coba username lain')
            return redirect(url_for('auth.register'))
        
        user = user.query.filter_by(email=email).first()
        if user:
            flash('email sudah ada', 'coba email lain')
            return redirect(url_for('auth.register'))
        
        user_baru = user(
            username=username,
            email=email,
            password=password,
            role='customer',
            alamat='belum diisi',
            no_hp='belum diisi',
            avatar='default.png',
            )

        user_baru.set_password(password)
        db.session.add(user_baru)
        db.session.commit()
        flash('registrasi berhasil', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_valo.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout', 'success')
    return redirect(url_for('auth.login'))