# Stock Portfolio Tracker — Web App

A full-stack version of the CodeAlpha Python Internship Task 2 project.
Tracks a simulated stock portfolio using hardcoded share prices, stores your
holdings in a SQLite database, and lets you export your portfolio as CSV.

## Stack
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, vanilla JavaScript
- **Database:** SQLite (file-based, no setup required)

## Project structure
```
stock_portfolio_webapp/
├── app.py                # Flask backend & API routes
├── requirements.txt
├── templates/
│   └── index.html        # Main page
└── static/
    ├── style.css
    └── script.js
```

## Setup & run

1. (Recommended) Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python app.py
   ```

4. Open your browser at **http://127.0.0.1:5000**

A `portfolio.db` SQLite file will be created automatically on first run.

## Features
- Hardcoded reference prices for 7 stocks (AAPL, TSLA, GOOGL, AMZN, MSFT, NFLX, META)
- Add holdings (symbol + quantity) through a web form
- Holdings persist in a SQLite database (survive app restarts)
- Live-updating total investment value
- Remove individual holdings
- Export your portfolio summary as a CSV file

## API routes
| Method | Route              | Description                        |
|--------|---------------------|-------------------------------------|
| GET    | `/api/stocks`        | Get the hardcoded price list        |
| GET    | `/api/portfolio`     | Get current holdings + total value  |
| POST   | `/api/add`            | Add a holding `{symbol, quantity}` |
| DELETE | `/api/remove/<id>`   | Remove a holding by id              |
| GET    | `/api/export`         | Download portfolio as CSV          |
