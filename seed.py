from app import create_app, db
from app.models import Product,user

app = create_app()

with app.app_context():
    print("lagi memuat derr.....")

    if not user.query.filter_by(username='admin1').first():
        user_admin = user(
            username='admin1',
            email='Mifzal22107@gmail.com',
            role='admin',
            no_hp='089679441438',
            alamat='Jl. Mediterania No. 1',
            avatar='default.png',
        )
        user_admin.set_password('admingantenk123')
        db.session.add(user_admin)
        db.session.commit()
        print("Admin berhasil ditambahkan")
    else:
        print("Admin sudah ada, skip")

print('udah der')