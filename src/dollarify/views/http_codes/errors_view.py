from flask import render_template

from dollarify.dollarify import app


@app.errorhandler(404)
def page_not_found(error):
    return '<p>Page not found</p>'