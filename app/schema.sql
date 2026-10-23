CREATE TABLE IF NOT EXISTS centres (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE,
    county      TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS farmers (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_no   TEXT NOT NULL UNIQUE,
    name        TEXT NOT NULL,
    phone       TEXT NOT NULL UNIQUE,
    centre_id   INTEGER NOT NULL REFERENCES centres(id),
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS deliveries (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id       INTEGER NOT NULL REFERENCES farmers(id),
    centre_id       INTEGER NOT NULL REFERENCES centres(id),
    clerk           TEXT NOT NULL,
    kg              REAL NOT NULL CHECK (kg > 0),
    status          TEXT NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending', 'confirmed', 'disputed')),
    farmer_kg       REAL,
    dispute_reason  TEXT,
    weighed_at      TEXT NOT NULL,
    resolved_at     TEXT
);

CREATE TABLE IF NOT EXISTS sms_outbox (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    phone       TEXT NOT NULL,
    message     TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_deliveries_farmer ON deliveries(farmer_id, weighed_at);
CREATE INDEX IF NOT EXISTS idx_deliveries_status ON deliveries(status);
