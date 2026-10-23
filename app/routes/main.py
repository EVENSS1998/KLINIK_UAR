from flask import Blueprint

valo = Blueprint('main', __name__)


@valo.route('/')
def index():
    return 'Hello World!'
