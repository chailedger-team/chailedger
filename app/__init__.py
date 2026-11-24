"""ChaiLedger application factory.

Each business area (farmers, deliveries, payments, notifications) lives in its
own package with a service layer (logic + data access) and a routes layer
(HTTP). Keeping them separate means any one of them can later be lifted out
into its own microservice.
"""

import logging
import time

from flask import Flask, jsonify

from app import db
from app.config import Config
from app.errors import register_error_handlers


def create_app(config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    register_error_handlers(app)

    from app.farmers.routes import bp as farmers_bp
    from app.deliveries.routes import bp as deliveries_bp
    from app.payments.routes import bp as payments_bp
    from app.notifications.routes import bp as notifications_bp

    app.register_blueprint(farmers_bp)
    app.register_blueprint(deliveries_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(notifications_bp)

    @app.get("/")
    def index():
        endpoints = sorted(
            f"{','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))} {rule.rule}"
            for rule in app.url_map.iter_rules()
            if rule.endpoint != "static"
        )
        return jsonify(
            service="ChaiLedger",
            description=(
                "Transparent weighing and payment records"
                " for smallholder tea farmers"
            ),
            endpoints=endpoints,
        )

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.get("/readiness")
    def readiness():
        start = time.time()
        try:
            db.get_db().execute("SELECT 1")
            duration_ms = round((time.time() - start) * 1000, 2)
            app.logger.info(
                "readiness check passed in %s ms", duration_ms
            )
            return jsonify(
                status="ready",
                database="connected",
                response_ms=duration_ms,
            )
        except Exception as exc:
            duration_ms = round((time.time() - start) * 1000, 2)
            app.logger.error(
                "readiness check failed after %s ms: %s",
                duration_ms,
                exc,
            )
            return jsonify(
                status="not ready",
                database="unreachable",
                error=str(exc),
                response_ms=duration_ms,
            ), 503

    return app
