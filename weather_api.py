import requests

API_KEY = 'dadacf579e1607f1ab46d718b7b268b5'  # Your OpenWeatherMap API key
CITY = 'Jalandhar'  # Replace with your city or make it dynamic

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx, 5xx)
        
        data = response.json()

        # Check if the response contains the expected data
        if response.status_code == 200:
            temp = data['main']['temp']
            weather_condition = data['weather'][0]['main']
            return temp, weather_condition
        else:
            return None, "Error: Unable to fetch weather data"

    except requests.exceptions.RequestException as e:
        # Handle network or request errors
        return None, f"Error: {e}"
