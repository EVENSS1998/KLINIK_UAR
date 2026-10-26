from flask import Blueprint, render_template
from app.decorators import admin_required

admin_valo = Blueprint("admin", __name__)


@admin_valo.route("/")
@admin_required
def dashboard():
    return render_template("admin/dashboard.html")
