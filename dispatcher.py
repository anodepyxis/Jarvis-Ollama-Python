import speech_recognition as sr
import re
from JARVIS.skills import match_skill
from JARVIS.features import handle_feature_command

class CommandDispatcher:
    def __init__(self, tts, config, skills):
        self.tts = tts
        self.config = config
        self.skills = skills
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
        try:
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query.lower()
        except Exception as e:
            print("Sorry, I did not catch that.")
            return None

    def handle(self, command):
        command = command.strip().lower()
        # Try skills first
        if match_skill(command, self.skills, self.tts):
            return True
        # Try feature modules
        if handle_feature_command(command, self.tts, self.config):
            return True
        return False 