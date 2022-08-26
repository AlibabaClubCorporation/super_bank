from .services.general_bank_service import checking_credits_status
from config.celery import app


@app.task
def periodic_check_credit_status():
    checking_credits_status()