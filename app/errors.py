"""Shared error types and JSON error responses."""

from flask import jsonify


class ValidationError(Exception):
    """Raised when client input is invalid (HTTP 400)."""


class NotFoundError(Exception):
    """Raised when a requested record does not exist (HTTP 404)."""


class ConflictError(Exception):
    """Raised when an action is not allowed in the record's current state (HTTP 409)."""


def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def _validation(err):
        return jsonify(error=str(err)), 400

    @app.errorhandler(NotFoundError)
    def _not_found(err):
        return jsonify(error=str(err)), 404

    @app.errorhandler(ConflictError)
    def _conflict(err):
        return jsonify(error=str(err)), 409

    @app.errorhandler(404)
    def _route_not_found(_err):
        return jsonify(error="Endpoint not found"), 404

    @app.errorhandler(405)
    def _method_not_allowed(_err):
        return jsonify(error="Method not allowed"), 405
