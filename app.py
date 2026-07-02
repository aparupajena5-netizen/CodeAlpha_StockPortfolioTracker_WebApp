"""
Stock Portfolio Tracker - Web App (Full Stack version)
CodeAlpha Python Programming Internship - Task 2 (extended)

Backend: Flask + SQLite
Frontend: HTML / CSS / JS (templates/index.html, static/style.css, static/script.js)

Run with:
    python app.py
Then open http://127.0.0.1:5000 in your browser.
"""

import csv
import io
import sqlite3
from datetime import datetime

from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)
DB_PATH = "portfolio.db"

# Hardcoded stock prices (per share, in USD) - same concept as the console version
STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 140,
    "AMZN": 145,
    "MSFT": 410,
    "NFLX": 640,
    "META": 480,
}


def get_db():
    """Open a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the holdings table if it doesn't already exist."""
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS holdings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            added_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def calculate_holdings():
    """
    Read all holdings from the database, merge duplicate symbols,
    and attach price/value info. Returns (holdings_list, total_value).
    """
    conn = get_db()
    rows = conn.execute("SELECT id, symbol, quantity FROM holdings ORDER BY id").fetchall()
    conn.close()

    holdings = []
    total_value = 0
    for row in rows:
        price = STOCK_PRICES.get(row["symbol"], 0)
        value = price * row["quantity"]
        total_value += value
        holdings.append(
            {
                "id": row["id"],
                "symbol": row["symbol"],
                "quantity": row["quantity"],
                "price": price,
                "value": value,
            }
        )
    return holdings, total_value


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/api/stocks")
def api_stocks():
    """Return the hardcoded stock price list, so the frontend can display it."""
    return jsonify(STOCK_PRICES)


@app.route("/api/portfolio")
def api_portfolio():
    """Return the current portfolio (holdings + total value)."""
    holdings, total_value = calculate_holdings()
    return jsonify({"holdings": holdings, "total_value": total_value})


@app.route("/api/add", methods=["POST"])
def api_add():
    """Add a new holding to the database."""
    data = request.get_json(force=True)
    symbol = str(data.get("symbol", "")).strip().upper()
    quantity = data.get("quantity")

    if symbol not in STOCK_PRICES:
        return jsonify({"error": f"'{symbol}' is not a recognized stock."}), 400

    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"error": "Quantity must be a positive whole number."}), 400

    conn = get_db()
    conn.execute(
        "INSERT INTO holdings (symbol, quantity, added_at) VALUES (?, ?, ?)",
        (symbol, quantity, datetime.now().isoformat(timespec="seconds")),
    )
    conn.commit()
    conn.close()

    holdings, total_value = calculate_holdings()
    return jsonify({"holdings": holdings, "total_value": total_value})


@app.route("/api/remove/<int:holding_id>", methods=["DELETE"])
def api_remove(holding_id):
    """Remove a single holding by its database id."""
    conn = get_db()
    conn.execute("DELETE FROM holdings WHERE id = ?", (holding_id,))
    conn.commit()
    conn.close()

    holdings, total_value = calculate_holdings()
    return jsonify({"holdings": holdings, "total_value": total_value})


@app.route("/api/export")
def api_export():
    """Export the current portfolio as a downloadable CSV file."""
    holdings, total_value = calculate_holdings()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Symbol", "Quantity", "Price", "Value"])
    for h in holdings:
        writer.writerow([h["symbol"], h["quantity"], h["price"], h["value"]])
    writer.writerow(["Total", "", "", total_value])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=portfolio_summary.csv"},
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
