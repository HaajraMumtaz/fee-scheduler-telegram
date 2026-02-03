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
from enum import Enum as PyEnum
from sqlalchemy import Enum



class PaymentState(PyEnum):
    unpaid = "unpaid"
    paid = "paid"

class PaymentReminder(Base):
    __tablename__ = "payment_reminders"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    sent_on = Column(Date, nullable=False)
    channel = Column(String)  # telegram / whatsapp / sms
    message_number = Column(Integer)  # 1, 2, 3, 4, ...

    student = relationship("Student")

class PayrollStatus(PyEnum):
    draft = "draft"
    approved = "approved"
    paid = "paid"

class TeachingAssignment(Base):
    __tablename__ = "teaching_assignments"

    id = Column(Integer, primary_key=True)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)

    subject = Column(String, nullable=False)
    lessons_per_month = Column(Integer, nullable=False)
    rate_per_lesson = Column(Float, nullable=False)

    student = relationship("Student", back_populates="assignments")
    teacher = relationship("Teacher", back_populates="assignments")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    fee_due_date = Column(Date, nullable=False)
    payment_state = Column(Enum(PaymentState), default=PaymentState.unpaid)

    poc_name = Column(String)
    poc_phone = Column(String)

    assignments = relationship("TeachingAssignment", back_populates="student")
    payments = relationship("StudentPayment", back_populates="student")
class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)  # will come from sheet
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    status = Column(String, default="active")

    assignments = relationship("TeachingAssignment", back_populates="teacher")
    payrolls = relationship("PayrollRun", back_populates="teacher")



class StudentPayment(Base):
    __tablename__ = "student_payments"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))

    amount = Column(Float, nullable=False)
    paid_on = Column(Date, nullable=False)

    student = relationship("Student", back_populates="payments")


class PayrollRun(Base):
    __tablename__ = "payroll_runs"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))

    month = Column(String, nullable=False)  # "2025-01"
    total_amount = Column(Float, nullable=False)

    status = Column(Enum(PayrollStatus), default=PayrollStatus.draft)

    teacher = relationship("Teacher", back_populates="payrolls")
class TeachingException(Base):
    __tablename__ = "teaching_exceptions"

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("teaching_assignments.id"))

    date = Column(Date, nullable=False)
    reason = Column(String)
    lessons_missed = Column(Integer, default=1)
