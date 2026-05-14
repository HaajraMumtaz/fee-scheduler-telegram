from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import (
    auth,
    dashboard,
    students,
    teachers,
    payroll,
    reminders,
    reports,
    cron,
    users,
    fees,
    base,
)

app = FastAPI(title="Academy Billing System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # tighten in production
    allow_credentials=True,                   # required for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(fees.router)
app.include_router(payroll.router)
app.include_router(reminders.router)
app.include_router(reports.router)
app.include_router(users.router)
app.include_router(cron.router)
app.include_router(base.router)