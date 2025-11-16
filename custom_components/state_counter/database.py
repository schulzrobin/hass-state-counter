import os
import sqlite3
from .const import DB_FILENAME, TABLE_NAME

class StateCounterDB:
    def __init__(self, hass_config_path: str):
        self.db_path = os.path.join(hass_config_path, DB_FILENAME)
        self._ensure_db()

    def _ensure_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                entity_id TEXT PRIMARY KEY,
                count INTEGER NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()

    def increment(self, entity_id: str) -> int:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(f"SELECT count FROM {TABLE_NAME} WHERE entity_id = ?", (entity_id,))
        row = c.fetchone()

        if row:
            new_count = row[0] + 1
            c.execute(f"UPDATE {TABLE_NAME} SET count = ? WHERE entity_id = ?", (new_count, entity_id))
        else:
            new_count = 1
            c.execute(f"INSERT INTO {TABLE_NAME} (entity_id, count) VALUES (?, ?)", (entity_id, new_count))

        conn.commit()
        conn.close()
        return new_count

    def get_count(self, entity_id: str) -> int:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(f"SELECT count FROM {TABLE_NAME} WHERE entity_id = ?", (entity_id,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else 0