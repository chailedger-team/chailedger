"""Monthly statement and payout estimate for a farmer.

Only confirmed kilograms count towards the estimated payout. Pending and
disputed kilograms are shown separately so the farmer can see exactly what
is still unresolved.
"""

from app.db import get_db
from app.farmers import service as farmers


def calculate_payout(confirmed_kg, rate_per_kg):
    return round(confirmed_kg * rate_per_kg, 2)


def monthly_statement(farmer_id, month, rate_per_kg):
    farmer = farmers.get_farmer(farmer_id)
    rows = get_db().execute(
        """SELECT id, weighed_at, kg, status, farmer_kg, clerk
           FROM deliveries
           WHERE farmer_id = ? AND substr(weighed_at, 1, 7) = ?
           ORDER BY weighed_at, id""",
        (farmer_id, month),
    ).fetchall()
    deliveries = [dict(r) for r in rows]

    totals = {"confirmed": 0.0, "pending": 0.0, "disputed": 0.0}
    for d in deliveries:
        totals[d["status"]] += d["kg"]
    totals = {k: round(v, 2) for k, v in totals.items()}

    return {
        "farmer_no": farmer["farmer_no"],
        "farmer_name": farmer["name"],
        "centre_name": farmer["centre_name"],
        "month": month,
        "deliveries": deliveries,
        "kg_confirmed": totals["confirmed"],
        "kg_pending": totals["pending"],
        "kg_disputed": totals["disputed"],
        "rate_per_kg": rate_per_kg,
        "estimated_payout": calculate_payout(totals["confirmed"], rate_per_kg),
        "currency": "KES",
    }
