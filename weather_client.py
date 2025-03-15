from dotenv import load_dotenv
import requests
import os

def get_api_key():
    load_dotenv()
    API_KEY = os.getenv("API_KEY")

def get_weather_data(location, date1=None, date2=None):
    pass 

if __name__ == "__main__":
    API_KEY = get_api_key()