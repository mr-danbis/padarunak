from routes.home import bp as home_bp
from routes.wishlist import bp as wishlist_bp
from routes.link_preview import bp as link_preview_bp


def register_routes(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(link_preview_bp)
