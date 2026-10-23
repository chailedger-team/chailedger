"""Business logic for recording weighings and confirming or disputing them.

Lifecycle of a delivery:
    pending  -> confirmed   (farmer agrees with the scale reading)
    pending  -> disputed    (farmer reports a different weight)
Only pending deliveries can change state, so a record cannot be quietly
edited after the farmer has responded.
"""

from datetime import datetime

from app.db import get_db
from app.errors import ConflictError, NotFoundError, ValidationError
from app.farmers import service as farmers
from app.notifications import service as notifications

STATUSES = ("pending", "confirmed", "disputed")


def record_delivery(farmer_id, kg, clerk, weighed_at, centre_id=None):
    farmer = farmers.get_farmer(farmer_id)
    centre_id = centre_id or farmer["centre_id"]
    centre = farmers.get_centre(centre_id)

    db = get_db()
    cur = db.execute(
        """INSERT INTO deliveries (farmer_id, centre_id, clerk, kg, weighed_at)
           VALUES (?, ?, ?, ?, ?)""",
        (farmer_id, centre_id, clerk, kg, weighed_at),
    )
    db.commit()
    delivery = get_delivery(cur.lastrowid)

    notifications.send_sms(
        farmer["phone"],
        f"ChaiLedger: {kg:g} kg of green leaf recorded for {farmer['farmer_no']} "
        f"at {centre['name']} by clerk {clerk} on {weighed_at[:16].replace('T', ' ')}. "
        f"Ref #{delivery['id']}. Reply 1 to confirm or 2 to dispute.",
    )
    return delivery


def get_delivery(delivery_id):
    row = get_db().execute(
        """SELECT d.*, f.farmer_no, f.name AS farmer_name, c.name AS centre_name
           FROM deliveries d
           JOIN farmers f ON f.id = d.farmer_id
           JOIN centres c ON c.id = d.centre_id
           WHERE d.id = ?""",
        (delivery_id,),
    ).fetchone()
    if row is None:
        raise NotFoundError(f"Delivery {delivery_id} not found")
    return dict(row)


def list_deliveries(status=None, farmer_id=None, centre_id=None):
    if status is not None and status not in STATUSES:
        raise ValidationError(f"'status' must be one of: {', '.join(STATUSES)}")
    sql = """SELECT d.*, f.farmer_no, f.name AS farmer_name, c.name AS centre_name
             FROM deliveries d
             JOIN farmers f ON f.id = d.farmer_id
             JOIN centres c ON c.id = d.centre_id
             WHERE 1 = 1"""
    params = []
    for column, value in (("d.status", status), ("d.farmer_id", farmer_id), ("d.centre_id", centre_id)):
        if value is not None:
            sql += f" AND {column} = ?"
            params.append(value)
    rows = get_db().execute(sql + " ORDER BY d.weighed_at DESC, d.id DESC", params).fetchall()
    return [dict(r) for r in rows]


def _resolve(delivery_id, new_status, farmer_kg=None, reason=None):
    delivery = get_delivery(delivery_id)
    if delivery["status"] != "pending":
        raise ConflictError(f"Delivery {delivery_id} is already {delivery['status']} and cannot be changed")
    db = get_db()
    db.execute(
        """UPDATE deliveries
           SET status = ?, farmer_kg = ?, dispute_reason = ?, resolved_at = ?
           WHERE id = ? AND status = 'pending'""",
        (new_status, farmer_kg, reason, datetime.now().isoformat(timespec="seconds"), delivery_id),
    )
    db.commit()
    return get_delivery(delivery_id)


def confirm_delivery(delivery_id):
    return _resolve(delivery_id, "confirmed")


def dispute_delivery(delivery_id, farmer_kg, reason):
    delivery = _resolve(delivery_id, "disputed", farmer_kg, reason)
    farmer = farmers.get_farmer(delivery["farmer_id"])
    notifications.send_sms(
        farmer["phone"],
        f"ChaiLedger: your dispute for Ref #{delivery_id} has been logged "
        f"(scale {delivery['kg']:g} kg, you reported {farmer_kg:g} kg). "
        "This weight is on hold until it is reviewed.",
    )
    return delivery


def dispute_report():
    """Disputes grouped by clerk and centre, to help spot problem scales or clerks."""
    rows = get_db().execute(
        """SELECT d.clerk,
                  c.name AS centre_name,
                  COUNT(*) AS total_deliveries,
                  SUM(d.status = 'disputed') AS disputed,
                  ROUND(SUM(CASE WHEN d.status = 'disputed'
                                 THEN d.farmer_kg - d.kg ELSE 0 END), 2) AS kg_gap
           FROM deliveries d JOIN centres c ON c.id = d.centre_id
           GROUP BY d.clerk, c.name
           ORDER BY disputed DESC, kg_gap DESC"""
    ).fetchall()
    report = []
    for r in rows:
        item = dict(r)
        item["dispute_rate"] = round(item["disputed"] / item["total_deliveries"], 2)
        report.append(item)
    return report
