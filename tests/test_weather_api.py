import requests

def get_response():
    response = requests.get("http://127.0.0.1:5000/weather")

    status_code = response.status_code

    if status_code == 200:
        print(response.json())
        
    else:
        print(f"Failed, error message : {status_code}")

if __name__ == "__main__":
    get_response()