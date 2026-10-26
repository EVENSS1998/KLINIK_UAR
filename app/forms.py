from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, FloatField, TextAreaField, SelectMultipleField 
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Masuk')


class RegistrasiForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=64)])
    confirm_password = PasswordField('Konfirmasi Password', validators=[DataRequired(), EqualTo('password',message='Password tidak cocok')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    no_hp = StringField('Nomor HP', validators=[DataRequired(), DataRequired()])

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    alamat = TextAreaField('Alamat', validators=[DataRequired()])
    no_hp = StringField('Nomor HP', validators=[DataRequired(), DataRequired()])
    avatar = FileField('Foto Profil', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Simpan Perubahan')


class ProductForm(FlaskForm):
    nama = StringField('Nama Barang', validators=[DataRequired()])
    harga = FloatField('Harga', validators=[DataRequired(), NumberRange(min=0)])
    stok = IntegerField('Stok', validators=[DataRequired(), NumberRange(min=0)])
    kategori = StringField('Kategori', validators=[DataRequired()])
    gambar = FileField('Gambar', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Tambah Barang')

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    ulasan = TextAreaField('Ulasan', validators=[DataRequired()])
    komentar = StringField('Komentar', validators=[DataRequired()])
    submit = SubmitField('Kirim Ulasan')

class CheckoutForm(FlaskForm):
    alamat = TextAreaField('Alamat', validators=[DataRequired()])
    no_hp = StringField('Nomor HP', validators=[DataRequired(), DataRequired()])
    submit = SubmitField('Checkout')

class BuktiBayarForm(FlaskForm):
    bukti = FileField('Bukti Pembayaran',
        render_kw={'accept': 'image/*'},
        validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'File harus .jpg, .jpeg, atau .png')])
    submit = SubmitField('Kirim Bukti Pembayaran')