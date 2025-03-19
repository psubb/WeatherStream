FROM python:3.13

ADD requirements.txt .

RUN pip install -r requirements.txt

CMD ["python3", "weather_api.py"]