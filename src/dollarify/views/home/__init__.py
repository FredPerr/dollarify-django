from flask import Blueprint, abort


bp = Blueprint('home', __name__, template_folder='templates')


@bp.route('/')
def home():
    return '<p>Home page</p>'