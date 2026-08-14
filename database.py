"""
database.py
------------
Handles SQLite database setup and scan history storage.
"""

import sqlite3
from datetime import datetime

DB_PATH = "phishguard.db"


def init_db():
    """
    Creates the database and scans table if they don't exist.
    Called once when Flask starts.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            url       TEXT NOT NULL,
            prediction TEXT NOT NULL,
            risk_score REAL NOT NULL,
            confidence REAL NOT NULL,
            scanned_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_scan(url: str, prediction: str, risk_score: float, confidence: float):
    """
    Saves a scan result to the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scans (url, prediction, risk_score, confidence, scanned_at)
        VALUES (?, ?, ?, ?, ?)
    """, (url, prediction, risk_score, confidence, datetime.now().strftime("%Y-%m-%d %H:%M")))

    conn.commit()
    conn.close()


def get_recent_scans(limit: int = 10) -> list:
    """
    Returns the most recent scans, newest first.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT url, prediction, risk_score, confidence, scanned_at
        FROM scans
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "url": row[0],
            "prediction": row[1],
            "risk_score": row[2],
            "confidence": row[3],
            "scanned_at": row[4],
        }
        for row in rows
    ]


def get_stats() -> dict:
    """
    Returns total scan counts for the dashboard.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scans")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE prediction = 'phishing'")
    phishing = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE prediction = 'legitimate'")
    legitimate = cursor.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "phishing": phishing,
        "legitimate": legitimate,
    }