"""Configuration read from environment variables (see .env.example).

No secrets are hard-coded. Defaults are safe for local development only.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Path to the SQLite database file.
    DATABASE = os.getenv("CHAILEDGER_DATABASE", "instance/chailedger.db")

    # Example rate paid per kg of confirmed green leaf, in KES.
    # This is a placeholder for demonstration, not an official factory rate.
    RATE_PER_KG = float(os.getenv("CHAILEDGER_RATE_PER_KG", "25"))

    # Upper limit for a single weighing, to catch typing mistakes at the scale.
    MAX_KG_PER_DELIVERY = float(os.getenv("CHAILEDGER_MAX_KG_PER_DELIVERY", "150"))
