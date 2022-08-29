from config.celery import app

from .services.credit_service import checking_credits_status


@app.task
def periodic_check_credit_status():
    checking_credits_status()