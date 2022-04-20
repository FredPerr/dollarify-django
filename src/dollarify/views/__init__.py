def register_blueprints(app):
    from dollarify.views import home

    views = (home, )

    for view in views:
        app.register_blueprint(view.bp)


def register_error_handlers(app):
    # Uncomment below to register error handlers:
    # from dollarify.views import http_codes
    # app.register_error_handler(404, http_codes.page_not_found)
    pass



