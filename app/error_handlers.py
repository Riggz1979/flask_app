def register_error_handlers(app):
    # Error 404 customization
    @app.errorhandler(404)
    def page_not_found(_):
        return "<h1>Looks like you're lost</h1>", 404

    # Error 500 customization
    @app.errorhandler(500)
    def page_not_found(_):
        return "<h1>My bad...</h1>", 500
