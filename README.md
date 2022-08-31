The project of emulation of the main banking tasks:
- Account creation
- Making payments to other accounts
- Purchase
- Take a loan
- Ability to see messages on behalf of the bank, during actions for example (withdrawing money from the account for part of the loan)
- Ability to view / clear the history of payments, transfers and messages

-------------------------------------------------- -------------------------------------------------- ----------------------

* This project uses Docker, Celery, Celery-beat, Redis, Postgresql.

* All dependencies are listed in the project/requirements.txt file.

* Before starting the project, pay attention to the file ( .env ) where you need to specify the type of settings file.

To run use the command:
- " docker-compose -f .\docker-compose.yaml up --build " if you use config file type as "debug" in .env
- " docker-compose -f .\docker-compose.prod.yaml up --build " if you are using configuration file type as "product" in .env

After starting docker, inside in the root of the Django project you need to run migrations:
- python3 manage.py makemigrations
- python3 manage.py migrate

And the project will be ready.

* In debug settings mode, Django uses the sqlite database, while in product settings mode it uses the postgres database.