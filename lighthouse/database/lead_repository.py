import sqlite3
from pathlib import Path

from models.lead import Lead


DATABASE_PATH = Path(__file__).resolve().parent / "lighthouse.db"


class LeadRepository:
    def __init__(self) -> None:
        self._create_table()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(DATABASE_PATH)
        connection.row_factory = sqlite3.Row
        return connection

    def _create_table(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT NOT NULL,
                    website TEXT NOT NULL UNIQUE,
                    industry TEXT NOT NULL DEFAULT '',
                    country TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'New',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def add(self, lead: Lead) -> bool:
        try:
            with self._connect() as connection:
                connection.execute(
                    """
                    INSERT INTO leads (
                        company,
                        website,
                        industry,
                        country,
                        status
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        lead.company,
                        lead.website,
                        lead.industry,
                        lead.country,
                        lead.status,
                    ),
                )
            return True
        except sqlite3.IntegrityError:
            return False

    def count(self) -> int:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS total FROM leads"
            ).fetchone()

        return int(row["total"])


    def list_all(self) -> list[Lead]:
        with self._connect() as connection:
            rows = connection.execute(
            """
            SELECT company, website, industry, country, status
            FROM leads
            ORDER BY created_at DESC
            """
        ).fetchall()

        return [
        Lead(
            company=row["company"],
            website=row["website"],
            industry=row["industry"],
            country=row["country"],
            status=row["status"],
        )
        for row in rows
    ]