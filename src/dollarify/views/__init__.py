from flask import Blueprint, abort


home_bp = Blueprint('home', __name__, template_folder='templates')


@home_bp.route('/')
def home():
    abort(404)
    return '<p>Home page</p>'