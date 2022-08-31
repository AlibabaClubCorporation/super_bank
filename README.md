The project of emulation of the main banking tasks:
- Account creation
- Making payments to other accounts
- Shopping
- Taking out a loan
- Ability to see messages on behalf of the bank, during actions for example (withdrawing money from the account for part of the loan)
- Ability to view / clear the history of payments, transfers and messages

----------------------------------------------------------------------------------------------------------------------------

* This project uses Docker, Celery and Celery-beat.
- You must use "docker-compose up --build" to run it, or "docker-compose up" if the image has already been built.

* All dependencies are listed in project/requirements.txt .

* Before starting the project, pay attention to the ( manage.py | config/celery.py ) file
- There you need to specify the configuration file to use ( default configuration file for debug mode )