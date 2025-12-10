import sqlite3
import os

# ---------------------------------------------------------
# 1. Decide where the database file will live
# ---------------------------------------------------------
# We store the DB at:  school_automation/app/db/school.db
DB_PATH = os.path.join(os.path.dirname(__file__), "school.db")


def create_connection():
    """
    Creates a connection to the SQLite database.
    If school.db does not exist, it will be created automatically.
    """
    conn = sqlite3.connect(DB_PATH)
    return conn


def create_tables():
    """
    Creates all required tables for the system.
    """
    conn = create_connection()
    cur = conn.cursor()

    # ---------------------------------------------------------
    # STUDENTS TABLE
    # Each row = one student
    # ---------------------------------------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            start_date TEXT,
            class_name TEXT,
            fee_amount REAL NOT NULL,
            fee_due_date TEXT NOT NULL,
            payment_status TEXT DEFAULT 'unpaid',
            poc TEXT
        );
    """)

    # ---------------------------------------------------------
    # TEACHERS TABLE
    # Each row = one teacher
    # ---------------------------------------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            pay_per_student REAL NOT NULL
        );
    """)

    # ---------------------------------------------------------
    # MANY-TO-MANY RELATIONSHIP: teacher <-> students
    # This table links which teacher teaches which student
    #
    # Example:
    # teacher_id=2, student_id=10
    #
    # ---------------------------------------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS student_teacher (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            teacher_id INTEGER NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(teacher_id) REFERENCES teachers(id)
        );
    """)

    # ---------------------------------------------------------
    # TRANSACTIONS TABLE
    # Stores:
    # - when a fee is paid
    # - when teachers are paid
    # ---------------------------------------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            teacher_id INTEGER,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            type TEXT NOT NULL,           
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(teacher_id) REFERENCES teachers(id)
        );
    """)

    conn.commit()
    conn.close()
    print("Database & tables created successfully!")


if __name__ == "__main__":
    create_tables()
