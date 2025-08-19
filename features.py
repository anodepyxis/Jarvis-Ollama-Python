import re
from JARVIS.features_web import handle_web_command
from JARVIS.features_file import handle_file_command
from JARVIS.features_weather import handle_weather_command
from JARVIS.features_clock import handle_clock_command
from JARVIS.features_todo import handle_todo_command

def handle_feature_command(command, tts, config):
    # Try each feature handler in turn
    if handle_web_command(command, tts, config):
        return True
    if handle_file_command(command, tts, config):
        return True
    if handle_weather_command(command, tts, config):
        return True
    if handle_clock_command(command, tts, config):
        return True
    if handle_todo_command(command, tts, config):
        return True
    return False 