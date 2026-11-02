from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Product, Keranjang_item

cart_blue = Blueprint('cart', __name__)

@cart_blue.route('/')
@login_required
def index():

    items = Keranjang_item.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.harga * item.jumlah for item in items)
    return render_template('cart/index.html', items=items, total=total)

@cart_blue.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add(product_id):
    product = Product.query.get_or_404(product_id)
    jumlah = int(request.form.get('jumlah', 1))

    if jumlah < 1:
        flash('Jumlah tidak valid', 'danger')
        return redirect(url_for('main.product_detail', product_id=product_id))
    if jumlah > product.stok:
        flash('stok tidak mencukupi', 'danger')
        return redirect(url_for('main.product_detail', product_id=product_id))
        
    item = Keranjang_item.query.filter_by(user_id=current_user.id, product_id=product_id).first()     

    if item:
        item.jumlah += jumlah
        if item.jumlah > product.stok:
            item.jumlah = product.stok
    else: 

        item = Keranjang_item(user_id=current_user.id, product_id=product_id, jumlah=jumlah)
    db.session.add(item)
    db.session.commit()
    flash('Produk ditambahkan ke keranjang')
    return redirect(url_for('cart.index'))

@cart_blue.route('/update/<int:item_id>', methods=['POST'])
@login_required
def update(item_id):
    item = Keranjang_item.query.get_or_404(item_id)

    if item.user_id != current_user.id:
        flash('akses ditolak', 'danger')
        return redirect(url_for('cart.index'))

    jumlah = int(request.form.get('jumlah', 1))

    if jumlah <= 0:

        db.session.delete(item)
    else:
        if jumlah > item.product.stok:
            jumlah = item.product.stok
            flash(f'Stok maksimal adalah {item.product.stok}', 'warning')
        item.jumlah = jumlah
    
    db.session.commit()
    flash('Keranjang berhasil diperbarui')
    return redirect(url_for('cart.index'))

@cart_blue.route('/remove/<int:item_id>', methods=['POST'])
@login_required
def remove(item_id):
    item = Keranjang_item.query.get_or_404(item_id)

    if item.user_id != current_user.id:
        flash('Akses di tolak', 'danger')
        return redirect(url_for('cart.index'))
    
    db.session.delete(item)
    db.session.commit()
    flash('item di hapus dari keranjang', 'sukses')
    return redirect(url_for('cart.index'))