from flask import Flask
from markupsafe import escape
from dollarify.models import User


app = Flask(__name__)


@app.route('/')
def root():

    users = User.all(User)

    return f'<p>Hello {escape(str(users[0]))}</p>'