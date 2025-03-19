from dotenv import load_dotenv
import requests
import os

def get_api_key():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    return api_key

def get_weather_data(location, api_key):
    response = requests.get(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/next1days?key={api_key}")
    status_code = response.status_code
    
    if status_code == 200:
        result = response.json()
        # remove unwanted categories
        for i in ["latitude", "queryCost", "longitude", "address", "timezone", "tzoffset", "description", "alerts", "stations"]:
            result.pop(i, None)
        # remove unwanted categories from "days"
        allowed_keys = ["datetime", "temp", "precip", "precipprob", "snow", "winddir", "pressure", "visibility", "cloudcover"]
        for day in result["days"]:
            for key in list(day):
                if key == "hours":
                    # filter out the hours 
                    for hour in range(len(day[key])):
                        for info in list(day[key][hour]):
                            if info not in allowed_keys:
                                day[key][hour].pop(info, None)
                    continue
                if key != "datetime":
                    day.pop(key, None)
                    
        for key in list(result["currentConditions"].keys()):
            if key not in allowed_keys:
                result["currentConditions"].pop(key, None)
        
        return result
    else:
        print(f"Failed to retrieve, error message: {status_code}")
        return None
        

if __name__ == "__main__":
    api_key = get_api_key()
    print(get_weather_data("san_jose", api_key))