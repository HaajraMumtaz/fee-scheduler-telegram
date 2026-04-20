from fastapi import FastAPI

from app.routes import auth, dashboard, students, payroll, cron

app = FastAPI()

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(students.router)
app.include_router(payroll.router)
app.include_router(cron.router)