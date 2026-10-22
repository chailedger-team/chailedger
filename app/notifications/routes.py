"""HTTP endpoint to view the simulated SMS outbox."""

from flask import Blueprint, jsonify, request

from app.notifications import service
from app.validation import kenyan_phone

bp = Blueprint("notifications", __name__)


@bp.get("/notifications/outbox")
def outbox():
    phone = request.args.get("phone")
    if phone:
        phone = kenyan_phone(phone)
    return jsonify(service.list_outbox(phone))
