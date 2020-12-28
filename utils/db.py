import os
import sqlite3


def create_connection():
    DB_FILE_PATH = os.path.join(os.path.realpath(f'{__file__}/../databases/'), f'general.sqlite3')
    try:
        conn = sqlite3.connect(DB_FILE_PATH)
        cur = conn.cursor()
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_DATE )")
    except sqlite3.Error as e:
        raise e

    return conn, cur


def wipe_table(conn):
    DB_FILE_PATH = os.path.join(os.path.realpath(f'{__file__}/../databases/'), f'general.sqlite3')
    conn.execute("DELETE FROM notes")
    os.remove(DB_FILE_PATH)
    create_connection()
