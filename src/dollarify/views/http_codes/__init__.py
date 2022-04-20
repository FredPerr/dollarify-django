from flask import Blueprint, render_template
from markupsafe import Markup


errors_bp = Blueprint('errors', __name__, template_folder='templates')


@errors_bp.errorhandler(404)
def page_not_found(error):
    return '<p>Page not found</p>', 404 # TODO: Not working