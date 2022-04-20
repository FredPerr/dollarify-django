from flask import Blueprint


def page_not_found(error):
    return '<p>Page not found</p>', 404 # TODO: Not working