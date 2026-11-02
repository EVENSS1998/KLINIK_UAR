import uuid
from flask import Blueprint, render_template,redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Keranjang_item, Order, PesananItem
from app.forms import CheckoutForm, BuktiBayarForm
from app.utils import save_file

checkout_blue = Blueprint('checkout', __name__)

@checkout_blue.route('/', methods=['GET', 'POST'])
@login_required
def index():
    items = Keranjang_item.query.filter_by(user_id=current_user.id).all()

    if not items:
        flash('Keranjang kamu kosong, tidak bisa checkout.', 'warning')
        return redirect(url_for('cart.index'))
    
    total = sum(item.product.harga * item.jumlah for item in items)
    form = CheckoutForm()

    if form.validate_on_submit():

        for item in items:
            if item.jumlah > item.product.stok:
                flash(f'Stok {item.product.nama} tidak cukup. Sisa {item.product.stok}.', 'danger')
                return redirect(url_for('cart.index'))
        
        kode_trx = f"TRX-{uuid.uuid4().hex[:8].upper()}"
        order = Order(
            kode_transaksi=kode_trx, user_id=current_user.id, total_harga=total, alamat_pengiriman=form.alamat_pengiriman.data, status='menunggu_pembayaran'
        )

        db.session.add(order)
        db.session.flush()

        for item in items:
            db.session.add(PesananItem(
                order_id=order.id,
                product_id=item.product_id,
                jumlah=item.jumlah,
                harga_satuan=item.product.harga,
                subtotal=item.product.harga * item.jumlah
            ))
            
            item.product.stok -= item.jumlah
            db.session.delete(item)
        
        db.session.commit()
        flash('Check berhasil! Silahkan upload bukti pembayaran.', 'success')
        return redirect(url_for('checkout.upload_bukti', order_id=order.id))

    return render_template('checkout/index.html', items=items, total=total, form=form)

@checkout_blue.route('/upload-bukti/<int:order_id>', methods=['GET', 'POST'])
@login_required
def upload_bukti(order_id):
    order = Order.query.get_or_404(order_id)


    if order.user_id != current_user.id:
        flash('Akses ditolak.', 'danger')
        return redirect(url_for('main.index'))
    
    form = BuktiBayarForm()
    if form.validate_on_submit():
        filename = save_file(form.bukti_bayar.data, 'BUKTI_FOLDER')
        if not filename:
            flash('File tidak valid. Pastikan berupa gambar.', 'danger')
            return render_template('checkout/upload_bukti.html', order=order, form=form)
        
        order.bukti_bayar = filename
        order.status = 'menunggu_verifikasi'
        db.session.commit()

        flash('Bukti bayar berhasil diupload! Pesanan sedang diverifikasi admin.', 'success')
        return redirect(url_for('user.orders'))

    return render_template('checkout/upload_bukti.html', order=order, form=form)
    