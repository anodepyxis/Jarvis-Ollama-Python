import requests
from geopy.geocoders import Nominatim

def handle_weather_command(command, tts, config):
    if command.startswith("what's the weather in ") or command.startswith("what is the weather in ") or command.startswith("weather forecast for "):
        if "weather forecast for " in command:
            location_name = command.replace("weather forecast for ", "").strip()
        elif "what's the weather in " in command:
            location_name = command.replace("what's the weather in ", "").strip()
        else:
            location_name = command.replace("what is the weather in ", "").strip()
        geolocator = Nominatim(user_agent="jarvis-assistant")
        location = geolocator.geocode(location_name)
        if not location:
            tts.speak(f"Sorry, I couldn't find {location_name}.")
            return True
        lat, lon = location.latitude, location.longitude
        api_key = config.get('OPENWEATHER_API_KEY', 'YOUR_API_KEY_HERE')
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()
            if data.get('cod') != 200:
                tts.speak("Sorry, I couldn't get the weather for that location.")
                return True
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            city = data['name']
            tts.speak(f"The weather in {city} is {weather} with a temperature of {temp} degrees Celsius.")
        except Exception:
            tts.speak("Sorry, I couldn't get the weather forecast.")
        return True
    return False 