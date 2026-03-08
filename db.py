import sqlite3
from datetime import datetime

DB_NAME = "loan_history.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loan_decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            revenue REAL,
            ebitda REAL,
            debt REAL,
            equity REAL,
            interest REAL,
            dscr REAL,
            debt_to_equity REAL,
            ai_score REAL,
            credit_grade TEXT,
            pd REAL,
            risk_category TEXT,
            decision TEXT
        )
    """)

    conn.commit()
    conn.close()

def save_decision(metrics, ai_score, credit_grade, pd_value, risk_category, final_decision):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO loan_decisions
        (timestamp, revenue, ebitda, debt, equity, interest, dscr, debt_to_equity,
         ai_score, credit_grade, pd, risk_category, decision)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        float(metrics.get("Revenue", 0.0)),
        float(metrics.get("EBITDA", 0.0)),
        float(metrics.get("Debt", 0.0)),
        float(metrics.get("Equity", 0.0)),
        float(metrics.get("Interest", 0.0)),
        float(metrics.get("DSCR", 0.0)),
        float(metrics.get("Debt_to_Equity", 0.0)),
        float(ai_score),
        str(credit_grade),
        float(pd_value),
        str(risk_category),
        str(final_decision)
    ))

    conn.commit()
    conn.close()

def get_all_decisions(limit=200):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, timestamp, revenue, dscr, debt_to_equity, ai_score, pd, risk_category, decision
        FROM loan_decisions
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()
    return rows

def reset_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM loan_decisions")
    conn.commit()
    conn.close()
