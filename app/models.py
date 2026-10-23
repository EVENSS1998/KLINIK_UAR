from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(150), nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    stok = db.Column(db.Integer, nullable=False, default=0)
    kategori = db.Column(db.String(100), nullable=False)
    gambar = db.Column(db.String(255), nullable=False)
    tgl_dibuat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    reviews = db.relationship("lihat_review", backref="product", lazy=True)

    def __init__(self, nama, harga, stok, kategori, gambar):
        self.nama = nama
        self.harga = harga
        self.stok = stok
        self.kategori = kategori
        self.gambar = gambar

class user(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="customer")
    avatar = db.Column(db.String(255), nullable=False, default="default.png")
    alamat = db.Column(db.Text, nullable=False)
    no_hp = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    reviews = db.relationship("lihat_review", backref="users", lazy=True)
    orders = db.relationship("Order", backref="users", lazy=True)
    cart_items = db.relationship("Keranjang_item", backref="users", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class lihat_review(db.Model):
    __tablename__ = "lihat_review"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=False)
    komentar = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Keranjang_item(db.Model):
    __tablename__ = "keranjang_item"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    product = db.relationship("Product")

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    kode_transaksi = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    total_harga = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30), default="menunggu_pembayaran")
    bukti_bayar = db.Column(db.String(255), nullable=True)
    alamat_pengiriman = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    items = db.relationship("PesananItem", backref="order", lazy=True)

class PesananItem(db.Model):
    __tablename__ = "pesanan_item"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    harga_satuan = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    product = db.relationship("Product")