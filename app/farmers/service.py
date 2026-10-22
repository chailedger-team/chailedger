"""Business logic for buying centres and farmers."""

import sqlite3

from app.db import get_db
from app.errors import ConflictError, NotFoundError
from app.validation import kenyan_phone


def create_centre(name, county):
    db = get_db()
    try:
        cur = db.execute("INSERT INTO centres (name, county) VALUES (?, ?)", (name, county))
        db.commit()
    except sqlite3.IntegrityError:
        raise ConflictError(f"A buying centre named '{name}' already exists") from None
    return get_centre(cur.lastrowid)


def get_centre(centre_id):
    row = get_db().execute("SELECT * FROM centres WHERE id = ?", (centre_id,)).fetchone()
    if row is None:
        raise NotFoundError(f"Buying centre {centre_id} not found")
    return dict(row)


def list_centres():
    rows = get_db().execute("SELECT * FROM centres ORDER BY name").fetchall()
    return [dict(r) for r in rows]


def create_farmer(name, phone, centre_id):
    phone = kenyan_phone(phone)
    get_centre(centre_id)  # raises NotFoundError if the centre does not exist
    db = get_db()
    next_id = db.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM farmers").fetchone()[0]
    farmer_no = f"CL-{next_id:04d}"
    try:
        cur = db.execute(
            "INSERT INTO farmers (farmer_no, name, phone, centre_id) VALUES (?, ?, ?, ?)",
            (farmer_no, name, phone, centre_id),
        )
        db.commit()
    except sqlite3.IntegrityError:
        raise ConflictError(f"A farmer with phone {phone} is already registered") from None
    return get_farmer(cur.lastrowid)


def get_farmer(farmer_id):
    row = get_db().execute(
        """SELECT f.*, c.name AS centre_name
           FROM farmers f JOIN centres c ON c.id = f.centre_id
           WHERE f.id = ?""",
        (farmer_id,),
    ).fetchone()
    if row is None:
        raise NotFoundError(f"Farmer {farmer_id} not found")
    return dict(row)


def list_farmers(centre_id=None):
    sql = """SELECT f.*, c.name AS centre_name
             FROM farmers f JOIN centres c ON c.id = f.centre_id"""
    params = ()
    if centre_id is not None:
        sql += " WHERE f.centre_id = ?"
        params = (centre_id,)
    rows = get_db().execute(sql + " ORDER BY f.id", params).fetchall()
    return [dict(r) for r in rows]
