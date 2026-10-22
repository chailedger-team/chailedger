"""HTTP endpoints for deliveries."""

from flask import Blueprint, current_app, jsonify, request

from app.deliveries import service
from app.validation import json_body, kilograms, positive_int, required_text, timestamp

bp = Blueprint("deliveries", __name__)


@bp.post("/deliveries")
def record_delivery():
    data = json_body()
    centre_id = data.get("centre_id")
    delivery = service.record_delivery(
        farmer_id=positive_int(data.get("farmer_id"), "farmer_id"),
        kg=kilograms(data.get("kg"), "kg", current_app.config["MAX_KG_PER_DELIVERY"]),
        clerk=required_text(data, "clerk", 60),
        weighed_at=timestamp(data.get("weighed_at")),
        centre_id=positive_int(centre_id, "centre_id") if centre_id is not None else None,
    )
    return jsonify(delivery), 201


@bp.get("/deliveries")
def list_deliveries():
    args = request.args
    farmer_id = args.get("farmer_id")
    centre_id = args.get("centre_id")
    return jsonify(
        service.list_deliveries(
            status=args.get("status"),
            farmer_id=positive_int(farmer_id, "farmer_id") if farmer_id else None,
            centre_id=positive_int(centre_id, "centre_id") if centre_id else None,
        )
    )


@bp.get("/deliveries/<int:delivery_id>")
def get_delivery(delivery_id):
    return jsonify(service.get_delivery(delivery_id))


@bp.post("/deliveries/<int:delivery_id>/confirm")
def confirm_delivery(delivery_id):
    return jsonify(service.confirm_delivery(delivery_id))


@bp.post("/deliveries/<int:delivery_id>/dispute")
def dispute_delivery(delivery_id):
    data = json_body()
    delivery = service.dispute_delivery(
        delivery_id,
        farmer_kg=kilograms(data.get("farmer_kg"), "farmer_kg", current_app.config["MAX_KG_PER_DELIVERY"]),
        reason=required_text(data, "reason", 200),
    )
    return jsonify(delivery)


@bp.get("/reports/disputes")
def dispute_report():
    return jsonify(service.dispute_report())
