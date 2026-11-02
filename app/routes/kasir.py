from app.models import Product
from flask import Blueprint, render_template, redirect, url_for, flash, request, make_response
from flask_login import login_required, current_user
from sqlalchemy import func
from datetime import datetime
import calendar
from app.decorators import kasir_required
from app import db
from app.models import Order, Pengeluaran
from app.forms import PengeluaranForm
from xhtml2pdf import pisa
from io import BytesIO

kasir_blue = Blueprint('kasir', __name__)

@kasir_blue.route('/')
@kasir_required
def dashboard():

    total_masuk = db.session.query(func.sum(Order.total_harga)).filter(Order.status.in_(['dibayar', 'dikirim', 'selesai'])).scalar() or 0

    total_keluar = db.session.query(func.sum(Pengeluaran.jumlah)).scalar() or 0

    saldo = total_masuk - total_keluar

    riwayat_pengeluaran = Pengeluaran.query.order_by(Pengeluaran.tanggal.desc()).all()

    return render_template('kasir/dashboard.html', total_masuk=total_masuk, total_keluar=total_keluar, saldo=saldo, riwayat=riwayat_pengeluaran)

@kasir_blue.route('/pengeluaran/tambah', methods=['GET','POST'])
@kasir_required
def tambah_pengeluaran():
    form = PengeluaranForm()
    if form.validate_on_submit():
        pengeluaran = Pengeluaran(keterangan=form.keterangan.data, jumlah=form.jumlah.data)

        db.session.add(pengeluaran)
        db.session.commit()
        flash('Catatan pengeluaran berhasil ditambah!', 'success')
        return redirect(url_for('kasir.dashboard'))
    return render_template('kasir/tambah_pengeluaran.html', form=form)

@kasir_blue.route('/laporan/pdf')
@kasir_required
def laporan_pdf():
    bulan_ini = datetime.now().month
    tahun_ini = datetime.now().year

    Pengeluaran_bulan_ini = Pengeluaran.query.filter(
        func.extract('month', Pengeluaran.tanggal) == bulan_ini,
        func.extract('year', Pengeluaran.tanggal) == tahun_ini     
        ).all()

    html = render_template('kasir/laporan_pdf.html', Pengeluaran=Pengeluaran_bulan_ini, bulan=calendar.month_name[bulan_ini], tahun=tahun_ini)

    result = BytesIO()
    pdf = pisa.CreatePDF(html, dest=result)
    
    if not pdf.err:
        response = make_response(result.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=Laporan_Keuangan_{bulan_ini}_{tahun_ini}.pdf'
        return response
    
    flash('Gagal membuat PDF.', 'danger')
    return redirect(url_for('kasir.dashboard'))

@kasir_blue.route('/stok', methods=['GET', 'POST'])
@kasir_required
def kelola_stok():
    # Ambil semua produk
    produk_list = Product.query.all()
    
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        tambahan = int(request.form.get('tambahan', 0))
        
        product = Product.query.get_or_404(product_id)
        if tambahan > 0:
            product.stok += tambahan
            db.session.commit()
            flash(f'Berhasil menambah {tambahan} stok untuk {product.nama}.', 'success')
        else:
            flash('Jumlah tambahan stok harus lebih dari 0.', 'danger')
            
        return redirect(url_for('kasir.kelola_stok'))
        
    return render_template('kasir/kelola_stok.html', produk=produk_list)
    