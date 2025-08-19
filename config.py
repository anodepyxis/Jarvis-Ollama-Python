import os

def load_config():
    return {
        'OPENWEATHER_API_KEY': os.environ.get('OPENWEATHER_API_KEY', 'YOUR_API_KEY_HERE'),
        'OLLAMA_MODEL': os.environ.get('OLLAMA_MODEL', 'phi3'),
        'WAKE_WORD': os.environ.get('WAKE_WORD', 'jarvis'),
        # Add more config as needed
    } 