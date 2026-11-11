from app import create_app, db
from app.models import Product, user

app = create_app()

with app.app_context():
    print("Sedang memuat data...")

    # 1. Buat Admin (jika belum ada)
    if not user.query.filter_by(username='admin1').first():
        user_admin = user(
            username='admin1',
            email='Mifzal22197@gmail.com',
            role='admin',
            no_hp='089679441458',
            alamat='Jl. Mediterania No. 1',
            avatar='default.png',
        )
        user_admin.set_password('admingantenk123')
        db.session.add(user_admin)
        print("✅ Admin berhasil ditambahkan")
    else:
        print("ℹ️ Admin sudah ada, skip")

    # 2. Buat Produk Dummy (jika belum ada)
    if Product.query.count() == 0:
        produk_list = [
            Product(nama="Headphone Wireless Bass Pro", harga=350000, stok=15, kategori="Elektronik", gambar="headphone.jpg"),
            Product(nama="Sepatu Sneaker Casual Putih", harga=279000, stok=8, kategori="Pakaian", gambar="sneaker.jpg"),
            Product(nama="Jam Tangan Minimalis Pria", harga=195000, stok=12, kategori="Aksesoris", gambar="jam.jpg"),
            Product(nama="Tas Ransel Laptop Oxford", harga=220000, stok=5, kategori="Aksesoris", gambar="tas.jpg")
        ]
        db.session.bulk_save_objects(produk_list)
        print("✅ 4 Produk dummy berhasil ditambahkan")
    else:
        print("ℹ️ Produk sudah ada, skip")
    
    if not user.query.filter_by(username='kasir1').first():
        user_kasir = user(
            username='kasir1',
            email='kasir@gmail.com',
            role='kasir',
            no_hp='089999999999',
            alamat='Kantor Kasir',
            avatar='default.png',
        )
        user_kasir.set_password('kasir123')
        db.session.add(user_kasir)
        print("✅ Akun Kasir berhasil ditambahkan")

    db.session.commit()
    print("Selesai derr!")