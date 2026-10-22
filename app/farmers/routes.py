"""HTTP endpoints for buying centres and farmers."""

from flask import Blueprint, jsonify, request

from app.farmers import service
from app.validation import json_body, positive_int, required_text

bp = Blueprint("farmers", __name__)


@bp.post("/centres")
def create_centre():
    data = json_body()
    centre = service.create_centre(required_text(data, "name"), required_text(data, "county", 50))
    return jsonify(centre), 201


@bp.get("/centres")
def list_centres():
    return jsonify(service.list_centres())


@bp.post("/farmers")
def create_farmer():
    data = json_body()
    farmer = service.create_farmer(
        name=required_text(data, "name"),
        phone=data.get("phone"),
        centre_id=positive_int(data.get("centre_id"), "centre_id"),
    )
    return jsonify(farmer), 201


@bp.get("/farmers")
def list_farmers():
    centre_id = request.args.get("centre_id")
    if centre_id is not None:
        centre_id = positive_int(centre_id, "centre_id")
    return jsonify(service.list_farmers(centre_id))


@bp.get("/farmers/<int:farmer_id>")
def get_farmer(farmer_id):
    return jsonify(service.get_farmer(farmer_id))
