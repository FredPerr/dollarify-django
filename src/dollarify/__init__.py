from flask import Flask, render_template

from dollarify import settings
from dollarify import db
from dollarify.web.views.auth import bp as auth_bp


app = Flask(__name__, template_folder=settings.TEMPLATES_PARENT_DIR)
app.register_blueprint(auth_bp)


@app.route('/')
def home_view():
    return render_template('home.html', version=db.version())


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
