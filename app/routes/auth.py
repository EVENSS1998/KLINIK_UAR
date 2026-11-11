from datetime import datetime
import uuid
from app.forms import RegistrasiForm
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

            if not pengguna.is_active:
                flash('Akun telah dinonaktifkan oleh admin epen yang gantenks.', 'danger')
                return redirect(url_for('auth.login'))

            login_user(pengguna)
            pengguna.last_login = datetime.now()
            db.session.commit()

            if pengguna.role == 'kasir':
                return redirect(url_for('kasir.dashboard'))
            elif pengguna.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('main.index'))
        else:
            flash('salah username atau password', 'danger')
    
    return render_template('auth/login.html')

@auth_valo.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrasiForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        no_hp = form.no_hp.data
        
        cek_username = user.query.filter_by(username=username).first()
        if cek_username:
            flash('username sudah ada, coba username lain', 'danger')
            return redirect(url_for('auth.register'))
        
        cek_email = user.query.filter_by(email=email).first()
        if cek_email:
            flash('email sudah ada, coba email lain', 'danger')
            return redirect(url_for('auth.register'))
        
        cek_hp = user.query.filter_by(no_hp=no_hp).first()
        if cek_hp:
            flash('Nomro HP sudah terdaftar', 'danger')
            return redirect(url_for('auth.register'))
        
        user_baru = user(
            username=username,
            email=email,
            alamat='belum diisi',
            no_hp=no_hp,
            avatar='default.png',
        )

        user_baru.set_password(password)
        db.session.add(user_baru)
        db.session.commit()
        flash('registrasi berhasil', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)
    

@auth_valo.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout', 'success')
    return redirect(url_for('auth.login'))