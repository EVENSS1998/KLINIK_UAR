from app.decorators import admin_required
from flask import Blueprint

admin_valo = Blueprint("admin", __name__)


@admin_valo.route("/")
@admin_required
def dashboard():
  return render_template("dashboard.html")
