from app import create_app, db
from app import models

app = create_app()

with app.app_context():
    print("Menghapus semua tabel lama...")
    db.drop_all()
    print("Membuat tabel baru dengan kolom is_active...")
    db.create_all()
    print("Selesai! Database siap digunakan.")