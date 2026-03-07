import sqlite3
from pathlib import Path
from typing import Dict

DB_PATH = Path(__file__).parent / "database" / "pdf_metadata.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS papers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT UNIQUE,
        title TEXT,
        authors TEXT,
        journal TEXT,
        year TEXT,
        abstract TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_metadata_in_db(filename: str, data: Dict[str, str]) -> bool:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO papers (filename,title,authors,journal,year,abstract)
    VALUES (?,?,?,?,?,?)
    """,(filename,data["title"],data["authors"],data["journal"],data["year"], data["abstract"]))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"DB Insert Error: {e}")
        return False
    