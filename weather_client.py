from dotenv import load_dotenv
import requests
import os

def get_api_key():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    return api_key

def get_weather_data(location, api_key):
    response = requests.get(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/?key={api_key}&include=current")
    status_code = response.status_code
    
    if status_code == 200:
        # only take current Conditions
        result = response.json()["currentConditions"]
        # remove unwanted categories
        for i in ["datetimeEpoch", "solarradition", "solarenergy", "icon", "stations", "source", "sunriseEpoch", "sunsetEpoch"]:
            result.pop(i, None)
        return result
    else:
        print(f"Failed to retrieve, error message: {status_code}")
        return
        

if __name__ == "__main__":
    api_key = get_api_key()
    print(get_weather_data("san_jose", api_key))