import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "pdf_metadata.db"

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
    print("db initialized successfully")


def insert_metadata(data: dict):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO papers (filename,title,authors,journal,year,abstract)
    VALUES (?,?,?,?,?,?)
    """,(
        data["filename"],
        data["title"],
        data["authors"],
        data["journal"],
        data["year"],
        data["abstract"]
    ))

    conn.commit()
    conn.close()
