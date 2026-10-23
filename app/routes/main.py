from flask import Blueprint, abort, flash, redirect, url_for, render_template, request
from app import db
from app.models import Product, user, lihat_review, Keranjang_item, Order, PesananItem
from flask_login import login_user, logout_user, login_required, current_user
from app.decorators import admin_required

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
    return render_template('product_detail.html', product=product, ulasan=ulasan_list)

@valo.route('/about')
def about():
    return render_template('about.html')