from config.celery import app

from .services.general_bank_service import checking_credits_status



@app.task
def task_checking_credits_status():
    checking_credits_status()
