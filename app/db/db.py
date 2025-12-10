import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "fees.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        class TEXT,
        start_date TEXT,
        fee_amount REAL,
        fee_due_date TEXT,
        payment_status TEXT DEFAULT 'unpaid',
        poc_name TEXT,
        poc_phone TEXT
    );

    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        pay_per_student REAL,
        total_pay REAL DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS teacher_student (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER,
        student_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id),
        FOREIGN KEY (student_id) REFERENCES students(id)
    );

    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        teacher_id INTEGER,
        date_paid TEXT,
        amount REAL,
        teacher_paid INTEGER DEFAULT 0,
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (teacher_id) REFERENCES teachers(id)
    );
    """)

    conn.commit()
    conn.close()
