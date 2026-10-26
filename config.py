import os
from os import getenv
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    AVATAR_FOLDER = os.path.join(UPLOAD_FOLDER, 'avatars')
    BUKTI_FOLDER = os.path.join(UPLOAD_FOLDER, 'bukti')
    PRODUK_FOLDER = os.path.join(UPLOAD_FOLDER, 'produk')

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    