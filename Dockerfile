FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
COPY .env .env

RUN pip3 install -r requirements.txt
RUN mkdir -p /app/data/files/

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]