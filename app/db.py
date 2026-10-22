"""SQLite connection handling and schema setup."""

import os
import sqlite3

import click
from flask import current_app, g

SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_db():
    if "db" not in g:
        path = current_app.config["DATABASE"]
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        g.db = sqlite3.connect(path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_exc=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def init_db():
    with open(SCHEMA_FILE, encoding="utf-8") as f:
        get_db().executescript(f.read())


@click.command("init-db")
def init_db_command():
    """Create the database tables (safe to run more than once)."""
    init_db()
    click.echo("Database initialised.")


@click.command("seed")
def seed_command():
    """Load sample centres and farmers for a quick demo."""
    from app.farmers import service as farmers

    init_db()
    kiamokama = farmers.create_centre("Kiamokama Buying Centre", "Kisii")
    litein = farmers.create_centre("Litein Buying Centre", "Kericho")
    farmers.create_farmer("Mary Wanjiku", "0712345678", kiamokama["id"])
    farmers.create_farmer("John Kiprono", "+254722000111", litein["id"])
    click.echo("Seeded 2 buying centres and 2 farmers.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_command)
    # Make sure tables exist on startup so the app works on first run.
    with app.app_context():
        init_db()
