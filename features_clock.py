from geopy.geocoders import Nominatim
from datetime import datetime
import pytz

def handle_clock_command(command, tts, config):
    if command.startswith("what time is it in "):
        location_name = command.replace("what time is it in ", "").strip()
        geolocator = Nominatim(user_agent="jarvis-assistant")
        location = geolocator.geocode(location_name)
        if not location:
            tts.speak(f"Sorry, I couldn't find {location_name}.")
            return True
        # Use country-level time zone as fallback
        from pytz import country_timezones
        country_code = location.raw.get('address', {}).get('country_code', '').upper()
        if not country_code or country_code not in country_timezones:
            tts.speak(f"Sorry, I couldn't determine the timezone for {location_name}.")
            return True
        tz_name = country_timezones[country_code][0]
        tz = pytz.timezone(tz_name)
        now = datetime.now(tz)
        tts.speak(f"The time in {location_name} is {now.strftime('%H:%M on %A, %B %d, %Y')}")
        return True
    if command.startswith("show world clock"):
        if "for " in command:
            locations = [loc.strip() for loc in command.split("for ")[-1].split(",")]
        else:
            locations = ["London", "New York", "Tokyo"]
        for loc in locations:
            handle_clock_command(f"what time is it in {loc}", tts, config)
        return True
    return False 