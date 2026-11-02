from flask_wtf import form
from flask import Blueprint, abort, flash, redirect, url_for, render_template, request
from app import db
from app.models import Product, user, lihat_review, Keranjang_item, Order, PesananItem
from flask_login import login_user, logout_user, login_required, current_user
from app.decorators import admin_required
from app.forms import ReviewForm

valo = Blueprint('main', __name__)


@valo.route('/')
def index():
    keyword = request.args.get("q")
    kategori_pilihan = request.args.get("kategori")

    query = Product.query
    if keyword:
        query = query.filter(Product.nama.ilike(f"%{keyword}%"))
    if kategori_pilihan:
        query = query.filter_by(kategori=kategori_pilihan)

    produk_list = query.all()

    kategori_list = [k[0] for k in db.session.query(Product.kategori).distinct().all()]

    return render_template("index.html",
    products=produk_list,
    kategori=kategori_list,
    pencarian_query=keyword,
    kategori_pilihan=kategori_pilihan
)

@valo.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    ulasan_list = product.reviews
    form = ReviewForm()

    has_bought = False
    if current_user.is_authenticated:

        order_lunas = db.session.query(Order).join(PesananItem).filter(
            Order.user_id == current_user.id,
            PesananItem.product_id == product_id,
            Order.status.in_(['dibayar', 'dikirim', 'selesai'])
        ).first()

        if order_lunas:
            has_bought = True
    return render_template('product_detail.html', product=product, ulasan=ulasan_list, form=form, has_bought=has_bought)

@valo.route('/about')
def about():
    return render_template('about.html')

@valo.route('/product/<int:product_id>/review', methods=['POST'])
@login_required
def add_review(product_id):
    product = Product.query.get_or_404(product_id)

    order_lunas = db.session.query(Order).join(PesananItem).filter(
        Order.user_id == current_user.id,
        PesananItem.product_id == product_id,
        Order.status.in_(['dibayar', 'dikirim', 'selesai'])
    ).first()

    if not order_lunas:
        flash('anda harus membeli dan membayar produk ini terlebih dahulu sebelum memberikan ulasan.', 'danger')
        return redirect(url_for('main.product_detail', product_id=product_id))


    form = ReviewForm()

    if form.validate_on_submit():
        
        existing_review = lihat_review.query.filter_by(
            user_id=current_user.id, 
            product_id=product.id
        ).first()

        if existing_review:
            flash('Anda sudah memberikan ulasan untuk produk ini.', 'warning')
            return redirect(url_for('main.product_detail', product_id=product_id))

        ulasan_baru = lihat_review(
            user_id=current_user.id,
            product_id=product.id,
            rating=form.rating.data,
            review=form.review.data,
            komentar=form.komentar.data
        )
        db.session.add(ulasan_baru)
        db.session.commit()
        flash('Terima kasih! Ulasan Anda berhasil ditambahkan.', 'success')
    else:
        flash('Gagal menambahkan ulasan. Pastikan semua kolom terisi dengan benar.', 'danger')

    return redirect(url_for('main.product_detail', product_id=product_id))