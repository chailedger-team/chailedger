"""Small input-validation helpers shared by all modules."""

import re
from datetime import datetime

from flask import request

from app.errors import ValidationError


def json_body():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")
    return data


def required_text(data, field, max_len=100):
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"'{field}' is required")
    value = value.strip()
    if len(value) > max_len:
        raise ValidationError(f"'{field}' must be at most {max_len} characters")
    return value


def positive_int(value, field):
    if isinstance(value, bool):
        raise ValidationError(f"'{field}' must be a positive integer")
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValidationError(f"'{field}' must be a positive integer") from None
    if number <= 0 or (isinstance(value, float) and not value.is_integer()):
        raise ValidationError(f"'{field}' must be a positive integer")
    return number


def kilograms(value, field, max_kg):
    if isinstance(value, bool):
        raise ValidationError(f"'{field}' must be a number")
    try:
        kg = float(value)
    except (TypeError, ValueError):
        raise ValidationError(f"'{field}' must be a number") from None
    if kg <= 0:
        raise ValidationError(f"'{field}' must be greater than 0")
    if kg > max_kg:
        raise ValidationError(f"'{field}' cannot exceed {max_kg:g} kg in a single weighing")
    return round(kg, 2)


_KENYA_PHONE = re.compile(r"^(?:\+?254|0)([17]\d{8})$")


def kenyan_phone(value):
    """Normalise a Kenyan mobile number to +254XXXXXXXXX."""
    if not isinstance(value, str):
        raise ValidationError("'phone' is required")
    cleaned = re.sub(r"[\s-]", "", value)
    match = _KENYA_PHONE.match(cleaned)
    if not match:
        raise ValidationError("'phone' must be a Kenyan mobile number, e.g. 0712345678 or +254712345678")
    return "+254" + match.group(1)


def month(value):
    """Validate a YYYY-MM string; defaults to the current month."""
    if value in (None, ""):
        return datetime.now().strftime("%Y-%m")
    try:
        datetime.strptime(value, "%Y-%m")
    except (TypeError, ValueError):
        raise ValidationError("'month' must be in YYYY-MM format") from None
    return value


def timestamp(value):
    """Validate an ISO timestamp; defaults to now."""
    if value in (None, ""):
        return datetime.now().isoformat(timespec="seconds")
    try:
        return datetime.fromisoformat(value).isoformat(timespec="seconds")
    except (TypeError, ValueError):
        raise ValidationError("'weighed_at' must be an ISO date-time, e.g. 2026-10-22T08:30:00") from None
