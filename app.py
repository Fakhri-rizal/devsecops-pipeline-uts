"""Aplikasi Flask sederhana dengan login yang aman dari SQL Injection."""
import os
import sqlite3

from flask import Flask, request
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
DB_PATH = os.environ.get("DB_PATH", "users.db")

LOGIN_FORM = """
<h2>Login</h2>
<form method="post">
  <input name="username" placeholder="Username">
  <input name="password" type="password" placeholder="Password">
  <button type="submit">Masuk</button>
</form>
"""


def get_connection():
    """Membuat koneksi ke database SQLite."""
    return sqlite3.connect(DB_PATH)


def init_db():
    """Membuat tabel users dan satu akun admin jika belum ada."""
    with get_connection() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS users "
            "(username TEXT PRIMARY KEY, password_hash TEXT NOT NULL)"
        )
        conn.execute(
            "INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)",
            ("admin", generate_password_hash("supersecret")),
        )


@app.route("/", methods=["GET", "POST"])
def login():
    """Menampilkan form login dan memverifikasi kredensial."""
    if request.method == "GET":
        return LOGIN_FORM
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    with get_connection() as conn:
        row = conn.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    if row and check_password_hash(row[0], password):
        return "Login Berhasil"
    return "Login Gagal", 401


if __name__ == "__main__":
    init_db()
    app.run(host=os.environ.get("APP_HOST", "127.0.0.1"), port=5000)
