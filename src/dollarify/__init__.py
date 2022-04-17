from flask import Flask


from dollarify import db


app = Flask(__name__)


@app.route('/')
def home():
    return f'<p>{db.version}</p>'