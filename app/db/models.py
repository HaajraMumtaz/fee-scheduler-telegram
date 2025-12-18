from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
    Table
)
from sqlalchemy.orm import relationship
from .base import Base
import enum

class PaymentStatus(enum.Enum):
    unpaid = "unpaid"
    paid = "paid"
    overdue = "overdue"


class TransactionType(enum.Enum):
    student_fee = "student_fee"
    teacher_payment = "teacher_payment"

class StudentTeacher(Base):
    __tablename__ = "student_teacher"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    class_name = Column(String)
    start_date = Column(Date)

    fee_amount = Column(Float, nullable=False)
    fee_due_date = Column(Date, nullable=False)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.unpaid)

    poc_name = Column(String)
    poc_phone = Column(String)

    teachers = relationship(
        "Teacher",
        secondary="teacher_student",
        back_populates="students"
    )

    transactions = relationship("Transaction", back_populates="student")

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    pay_per_student = Column(Float, nullable=False)

    students = relationship(
        "Student",
        secondary="teacher_student",
        back_populates="teachers"
    )

    transactions = relationship("Transaction", back_populates="teacher")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    type = Column(enum(TransactionType), nullable=False)

    student_id = Column(Integer, ForeignKey("students.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))

    student = relationship("Student", back_populates="transactions")
    teacher = relationship("Teacher", back_populates="transactions")

teacher_student = Table(
    "teacher_student",
    Base.metadata,
    Column("teacher_id", ForeignKey("teachers.id"), primary_key=True),
    Column("student_id", ForeignKey("students.id"), primary_key=True),
)