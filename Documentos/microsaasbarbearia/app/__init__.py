import os
from flask import Flask, request, url_for, abort
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

load_dotenv()

from app.config import config_map
from app.extensions import db, login_manager, migrate


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf = CSRFProtect(app)

    # Exempt auth routes (login/register don't have CSRF yet)
    csrf.exempt("api.api_bp")
    csrf.exempt("payments.webhook_mercadopago")

    # Security headers
    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' https://cdn.tailwindcss.com https://cdn.jsdelivr.net 'unsafe-inline' 'unsafe-hashes'; "
            "style-src 'self' https://cdn.tailwindcss.com https://cdn.jsdelivr.net https://fonts.googleapis.com 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://fonts.gstatic.com;"
        )
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.appointments import appointments_bp
    from app.routes.clients import clients_bp
    from app.routes.barbers import barbers_bp
    from app.routes.services import services_bp
    from app.routes.payments import payments_bp
    from app.routes.products import products_bp
    from app.routes.profile import profile_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(barbers_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(api_bp)

    # Serve uploaded files
    from flask import send_from_directory

    @app.route("/uploads/<path:subdir>/<path:filename>")
    def uploaded_file(subdir, filename):
        import os
        uploads_dir = os.path.join(app.root_path, "..", "uploads", subdir)
        return send_from_directory(uploads_dir, filename)

    return app
