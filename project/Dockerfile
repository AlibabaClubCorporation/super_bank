FROM python:3.10

RUN mkdir -p /usr/src/project/
WORKDIR /usr/src/project/

COPY . /usr/src/project/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8080" ]