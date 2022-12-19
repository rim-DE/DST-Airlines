FROM python:3.8-slim-buster

EXPOSE 8050

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "gunicorn", "--workers=1", "--threads=1", "-b 0.0.0.0:8050", "app:server"]
