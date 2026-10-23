"""HTTP endpoint for farmer statements."""

from flask import Blueprint, current_app, jsonify, request

from app.payments import service
from app.validation import month

bp = Blueprint("payments", __name__)


@bp.get("/farmers/<int:farmer_id>/statement")
def statement(farmer_id):
    return jsonify(
        service.monthly_statement(
            farmer_id,
            month(request.args.get("month")),
            current_app.config["RATE_PER_KG"],
        )
    )
