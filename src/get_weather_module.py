import requests

def get_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # Для отримання температури у градусах Цельсія
    }
    response = requests.get(base_url, params=params)
    return response.json()

def format_weather(weather_data):
    try:
        city = weather_data['name']
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        return f"Weather in {city}: {temp}°C, {description}"
    except KeyError:
        return "Couldn't retrieve weather information."

# Використання функції
if __name__ == '__main__':
    api_key = 'YOUR_API_KEY'  # Замініть на ваш API-ключ
    city = input("Enter city name: ")
    weather_data = get_weather(city, api_key)
    weather_report = format_weather(weather_data)
    print(weather_report)
