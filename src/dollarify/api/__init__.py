from flask import Flask
from markupsafe import escape


app = Flask(__name__)


@app.route('/')
def root():
    return f'<p>Hello World</p>'