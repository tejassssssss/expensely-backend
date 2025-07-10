import sqlite3
import csv
from datetime import datetime

# ✅ Initialize the database and create the expenses table
def init_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# ✅ Fetch all expenses
def get_all_expenses(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row[0],
            "title": row[1],
            "amount": row[2],
            "category": row[3],
            "date": row[4]
        }
        for row in rows
    ]

# ✅ Add a new expense
def add_expense(db_name, data):
    try:
        title = data.get("title")
        amount = data.get("amount")
        category = data.get("category")
        date = data.get("date")

        # 🔍 Check for missing or empty values
        if not title or not category or not date or amount is None:
            print("❌ Missing required fields:", data)
            return False

        # 🔢 Convert amount safely
        amount = float(amount)

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (title, amount, category, date) VALUES (?, ?, ?, ?)",
            (title, amount, category, date)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("❌ Error adding expense:", e)
        return False

# ✅ Delete a specific expense
def delete_expense(db_name, expense_id):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("❌ Error deleting expense:", e)
        return False

# ✅ Edit a specific expense
def edit_expense(db_name, expense_id, data):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE expenses 
               SET title = ?, amount = ?, category = ?, date = ?
               WHERE id = ?''',
            (
                data["title"],
                data["amount"],
                data["category"],
                data["date"],
                expense_id
            )
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("❌ Error editing expense:", e)
        return False

# ✅ Export expenses to CSV
def export_to_csv(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT title, amount, category, date FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()

    filename = f"expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Amount", "Category", "Date"])
        writer.writerows(rows)
    return filename

# ✅ Calculate summary (total and top category)
def get_summary(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT SUM(amount), category FROM expenses GROUP BY category ORDER BY SUM(amount) DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    total = sum(row[0] for row in rows)
    top_category = rows[0][1] if rows else None
    return total, top_category
