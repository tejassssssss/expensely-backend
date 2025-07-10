from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from datetime import timedelta
import sqlite3

from utils import (
    init_db, get_all_expenses, add_expense,
    delete_expense, export_to_csv, get_summary, edit_expense
)

app = Flask(__name__)

# App Configuration
app.secret_key = 'your-secret-key'

# CORS Setup
CORS(app,
     resources={r"/api/*": {"origins": "*"}},
     supports_credentials=True,
     expose_headers="Authorization",
     allow_headers=["Authorization", "Content-Type"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Initialize Tables
DB_NAME = "expense.db"
init_db(DB_NAME)


def init_users_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Home Route
@app.route("/")
def home():
    return "Expensely API is Running Without Login!"


@app.route("/api/expenses", methods=["GET"])
def get_expenses():
    expenses = get_all_expenses(DB_NAME)
    return jsonify(expenses)

@app.route("/api/add", methods=["POST"])
def add():
    data = request.get_json()
    success = add_expense(DB_NAME, data)
    return jsonify({"success": success}), (200 if success else 400)

@app.route("/api/delete/<int:expense_id>", methods=["DELETE"])
def delete(expense_id):
    success = delete_expense(DB_NAME, expense_id)
    return jsonify({"success": success})

@app.route("/api/edit/<int:expense_id>", methods=["PUT"])
def edit(expense_id):
    data = request.get_json()
    success = edit_expense(DB_NAME, expense_id, data)
    return jsonify({"success": success})

@app.route("/api/export", methods=["GET"])
def export():
    filename = export_to_csv(DB_NAME)
    return send_file(filename, as_attachment=True)

@app.route("/api/summary", methods=["GET"])
def summary():
    total, top_category = get_summary(DB_NAME)
    return jsonify({
        "total": total,
        "top_category": top_category
    })

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
