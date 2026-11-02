from werkzeug.datastructures import FileStorage
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Order, user
from app.forms import ProfileForm
from app.utils import save_file

user_blue = Blueprint('user', __name__)

@user_blue.route('/orders')
@login_required
def orders():

    daftar_pesanan = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('user/orders.html', orders=daftar_pesanan)

@user_blue.route('/orders/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)

    if order.user_id != current_user.id:
        flash('Akses ditolak.', 'danger')
        return redirect(url_for('user.orders'))
    return render_template('user/order_detail.html', order=order)

@user_blue.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():

        if form.no_hp.data != current_user.no_hp:
            cek_hp = user.query.filter_by(no_hp=form.no_hp.data).first()
            if cek_hp:
                flash('Nomor HP sudah di pakai.', 'danger')
                return redirect(url_for('user.profile'))
        
        if form.username.data != current_user.username:
            if user.query.filter_by(username=form.username.data).first():
                flash('username sudah ada', 'danger')
                return redirect(url_for('user.profile'))

            
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.alamat = form.alamat.data
        current_user.no_hp = form.no_hp.data

        if isinstance(form.avatar.data, FileStorage) and form.avatar.data.filename:
            filename = save_file(form.avatar.data, 'AVATAR_FOLDER')

            if filename:
                current_user.avatar = filename
            else:
                flash('Format gambar tidak valid. Gunakan JPG/PNG.', 'danger')
                return redirect(url_for('user.profile'))
        db.session.commit()
        flash('Profile berhasil diupdate!', 'success')
        return redirect(url_for('user.profile'))

    return render_template('user/profile.html', form=form)
    