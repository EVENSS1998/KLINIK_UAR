import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "silahkan login dulu ya pak/buk"
    login_manager.login_message_category = "danger"
    
    from app import models

    @login_manager.user_loader
    def load_user(user_id):
        return models.user.query.get(int(user_id))

    from app.routes.main import valo as main_valo
    from app.routes.admin import admin_valo
    from app.routes.auth import auth_valo
    # from app.routes.cart import cart_blue
    # from app.routes.checkout import checkout_blue

    app.register_blueprint(main_valo)
    app.register_blueprint(admin_valo, url_prefix='/admin')
    app.register_blueprint(auth_valo, url_prefix='/auth')
    # app.register_blueprint(cart_blue, url_prefix='/cart')
    # app.register_blueprint(checkout_blue, url_prefix='/checkout')
    
    return app
