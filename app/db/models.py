from .db import get_connection

class Student:
    @staticmethod
    def create(name, class_, start_date, fee_amount, fee_due_date, poc_name, poc_phone):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO students (name, class, start_date, fee_amount, fee_due_date, poc_name, poc_phone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, class_, start_date, fee_amount, fee_due_date, poc_name, poc_phone))
        conn.commit()
        conn.close()

    @staticmethod
    def all():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()
        conn.close()
        return rows


class Teacher:
    @staticmethod
    def create(name, pay_per_student):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO teachers (name, pay_per_student)
            VALUES (?, ?)
        """, (name, pay_per_student))
        conn.commit()
        conn.close()
