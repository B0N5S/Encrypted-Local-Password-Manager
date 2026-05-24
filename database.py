import sqlite3
import os
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "passsafe.db")
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
def initialise_database():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS master_user (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT NOT NULL,
            password_hash BLOB NOT NULL,
            salt          BLOB NOT NULL,
            created_at    TEXT DEFAULT (datetime('now'))
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vault_entries (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id       INTEGER NOT NULL,
            site_name     TEXT NOT NULL,
            site_url      TEXT,
            username      TEXT,
            password_enc  BLOB NOT NULL,
            notes         TEXT,
            category      TEXT DEFAULT 'General',
            created_at    TEXT DEFAULT (datetime('now')),
            updated_at    TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()
def master_user_exists():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM master_user")
    count = cur.fetchone()[0]
    conn.close()
    return count > 0
def create_master_user(username, password_hash, salt):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO master_user (username, password_hash, salt) VALUES (?, ?, ?)",
        (username, password_hash, salt)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id
def get_first_user():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM master_user LIMIT 1")
    row = cur.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None
def add_vault_entry(user_id, site_name, site_url, username, password_enc, notes, category):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO vault_entries
           (user_id, site_name, site_url, username, password_enc, notes, category)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (user_id, site_name, site_url, username, password_enc, notes, category)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id
def get_all_entries(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM vault_entries WHERE user_id = ? ORDER BY site_name ASC",
        (user_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]
def update_vault_entry(entry_id, site_name, site_url, username, password_enc, notes, category):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """UPDATE vault_entries
           SET site_name = ?,
               site_url  = ?,
               username  = ?,
               password_enc = ?,
               notes     = ?,
               category  = ?,
               updated_at = datetime('now')
           WHERE id = ?""",
        (site_name, site_url, username, password_enc, notes, category, entry_id)
    )
    conn.commit()
    conn.close()
def delete_vault_entry(entry_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM vault_entries WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()
def search_entries(user_id, query):
    conn = get_connection()
    cur = conn.cursor()
    like = "%" + query + "%"
    cur.execute(
        """SELECT * FROM vault_entries
           WHERE user_id = ?
           AND (site_name LIKE ? OR username LIKE ? OR site_url LIKE ? OR category LIKE ?)
           ORDER BY site_name ASC""",
        (user_id, like, like, like, like)
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]
