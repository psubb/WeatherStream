FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=app/weather_api.py

CMD ["python3", "app/weather_api.py"]