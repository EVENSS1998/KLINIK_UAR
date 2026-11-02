from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user
from sqlalchemy import func
from app.decorators import admin_required
from app import db
from app.models import Product, user, Order
from app.forms import ProductForm
from app.utils import save_file

admin_valo = Blueprint("admin", __name__)

@admin_valo.route("/")
@admin_required
def dashboard():
    total_products = db.session.query(func.count(Product.id)).scalar()
    total_users = db.session.query(func.count(user.id)).scalar()
    total_orders = db.session.query(func.count(Order.id)).scalar()

    total_sales = db.session.query(func.sum(Order.total_harga)).scalar() or 0
    menunggu_verifikasi = db.session.query(func.count(Order.id)).filter(Order.status == "menunggu_verifikasi").scalar()
    
    return render_template("admin/dashboard.html",
        total_produk=total_products,
        total_user=total_users,
        total_order=total_orders,
        total_pendapatan=total_sales,
        menunggu_verifikasi=menunggu_verifikasi
    )

@admin_valo.route("/orders")
@admin_required
def orders():
    daftar_order = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("admin/orders.html", orders=daftar_order)

@admin_valo.route("/orders/<int:order_id>")
@admin_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template("admin/order_detail.html", order=order)

@admin_valo.route("/order/<int:order_id>/approve", methods=["POST"])
@admin_required
def approve_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.status == "menunggu_verifikasi":
        order.status = 'dibayar'
        db.session.commit()
        flash(f"Pembayaran untuk pesanan {order.kode_transaksi} telah disetujui", "success")
    else: 
        flash(f"Pembayaran untuk pesanan {order.kode_transaksi} tidak ditemukan atau sudah diverifikasi", "danger")
    return redirect(url_for("admin.order_detail", order_id=order.id))

@admin_valo.route("/order/<int:order_id>/tolak", methods=["POST"])
@admin_required
def tolak_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.status == "menunggu_verifikasi":
        order.status = 'ditolak'
        db.session.commit()
        flash(f"Pembayaran untuk pesanan {order.kode_transaksi} ditolak", "danger")
    return redirect(url_for("admin.order_detail", order_id=order.id))

@admin_valo.route("/products")
@admin_required
def manage_products():
    produk = Product.query.all()
    return render_template("admin/manage_products.html", products=produk)

@admin_valo.route("/products/add", methods=['GET', 'POST'])
@admin_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        filename = save_file(form.gambar.data, 'PRODUK_FOLDER')
        if not filename:
            flash('Gambar wajib diupload dengan format JPG/PNG.', 'danger')
            return render_template("admin/product_form.html", form=form, title="Tambah Produk")
            
        produk = Product(
            nama=form.nama.data, harga=form.harga.data, 
            stok=form.stok.data, kategori=form.kategori.data, gambar=filename
        )
        db.session.add(produk)
        db.session.commit()
        flash('Produk berhasil ditambahkan!', 'success')
        return redirect(url_for('admin.manage_products'))
    return render_template("admin/product_form.html", form=form, title="Tambah Produk")

@admin_valo.route("/products/edit/<int:id>", methods=['GET', 'POST'])
@admin_required
def edit_product(id):
    produk = Product.query.get_or_404(id)
    form = ProductForm(obj=produk)
    if form.validate_on_submit():
        produk.nama = form.nama.data
        produk.harga = form.harga.data
        produk.stok = form.stok.data
        produk.kategori = form.kategori.data
        if form.gambar.data:
            filename = save_file(form.gambar.data, 'PRODUK_FOLDER')
            if filename:
                produk.gambar = filename
        db.session.commit()
        flash('Produk berhasil diupdate!', 'success')
        return redirect(url_for('admin.manage_products'))
    return render_template("admin/product_form.html", form=form, title="Edit Produk")

@admin_valo.route("/products/delete/<int:id>", methods=['POST'])
@admin_required
def delete_product(id):
    produk = Product.query.get_or_404(id)
    db.session.delete(produk)
    db.session.commit()
    flash('Produk berhasil dihapus!', 'success')
    return redirect(url_for('admin.manage_products'))

@admin_valo.route("/users")
@admin_required
def manage_users():
    semua_user = user.query.all()
    return render_template("admin/manage_users.html", users=semua_user)

@admin_valo.route("/users/delete/<int:id>", methods=['POST'])
@admin_required
def delete_user(id):
    if id == current_user.id:
        flash('Anda tidak bisa menghapus akun Anda sendiri!', 'danger')
    else:
        u = user.query.get_or_404(id)
        db.session.delete(u)
        db.session.commit()
        flash('User berhasil dihapus!', 'success')
    return redirect(url_for('admin.manage_users'))