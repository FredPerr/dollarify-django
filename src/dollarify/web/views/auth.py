from flask import render_template, Blueprint


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/sign-up/')
def sign_up_view():
    return render_template('auth/sign-up.html')