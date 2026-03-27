from pathlib import Path

from flask import Flask, jsonify, render_template_string, request, send_from_directory
from flask_cors import CORS

try:
    from .database import get_connection, init_db
except ImportError:
    from database import get_connection, init_db

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
CORS(app)
init_db()


@app.get("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/api/health")
def health():
    return jsonify({"ok": True})


@app.post("/api/messages")
def save_message():
    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip()
    message = (payload.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify({"error": "Name, email, and message are required."}), 400

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
            (name, email, message),
        )
        conn.commit()

    return jsonify({"success": True, "message": "Saved."}), 201


@app.get("/api/messages")
def list_messages():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name, email, message, created_at FROM messages ORDER BY id DESC"
        ).fetchall()
    return jsonify([dict(row) for row in rows])


@app.get("/admin")
def admin():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name, email, message, created_at FROM messages ORDER BY id DESC"
        ).fetchall()

    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Portfolio Admin</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 24px; background:#0f172a; color:#e2e8f0; }
            h1 { margin-bottom: 16px; }
            table { width: 100%; border-collapse: collapse; background: #111827; }
            th, td { border: 1px solid #334155; padding: 10px; text-align: left; vertical-align: top; }
            th { background: #1e293b; }
            .wrap { white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <h1>Contact Messages (Admin)</h1>
        <p>Total messages: {{ total }}</p>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Message</th>
                    <th>Created At</th>
                </tr>
            </thead>
            <tbody>
            {% for row in rows %}
                <tr>
                    <td>{{ row["id"] }}</td>
                    <td>{{ row["name"] }}</td>
                    <td>{{ row["email"] }}</td>
                    <td class="wrap">{{ row["message"] }}</td>
                    <td>{{ row["created_at"] }}</td>
                </tr>
            {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """
    return render_template_string(template, rows=rows, total=len(rows))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
