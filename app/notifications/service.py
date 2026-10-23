"""Simulated SMS gateway.

Messages are stored in an outbox table instead of being sent, so the feature
can be demonstrated without a paid SMS provider. Swapping this module for a
real gateway (e.g. Africa's Talking) later would not affect any other module.
"""

import logging

from app.db import get_db

log = logging.getLogger(__name__)


def send_sms(phone, message):
    db = get_db()
    cur = db.execute("INSERT INTO sms_outbox (phone, message) VALUES (?, ?)", (phone, message))
    db.commit()
    log.info("SMS to %s: %s", phone, message)
    return cur.lastrowid


def list_outbox(phone=None, limit=50):
    sql = "SELECT * FROM sms_outbox"
    params = []
    if phone:
        sql += " WHERE phone = ?"
        params.append(phone)
    sql += " ORDER BY id DESC LIMIT ?"
    params.append(limit)
    return [dict(r) for r in get_db().execute(sql, params).fetchall()]
