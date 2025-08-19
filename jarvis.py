import logging
import os
from JARVIS.config import load_config
from JARVIS.tts import TTSManager
from JARVIS.dispatcher import CommandDispatcher
from JARVIS.skills import load_skills

def main():
    config = load_config()
    logging.basicConfig(level=logging.INFO)
    tts = TTSManager()
    skills = load_skills()
    dispatcher = CommandDispatcher(tts, config, skills)
    tts.speak("Hello, I am your assistant. How can I help you?")
    conversation = []
    def save_conversation():
        file_path = input("Enter filename to save conversation: ").strip()
        if not file_path:
            print("Save cancelled.")
            return
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(conversation))
            print(f"Conversation saved to {file_path}.")
        except Exception as e:
            print(f"Failed to save: {e}")

    def load_conversation():
        file_path = input("Enter filename to load conversation: ").strip()
        if not file_path:
            print("Load cancelled.")
            return
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            print("\n--- Loaded Conversation ---")
            for line in lines:
                print(line.rstrip())
            print("--- End ---\n")
        except Exception as e:
            print(f"Failed to load: {e}")

    def show_help():
        print("""
JARVIS CLI Help
----------------
- Type your command and press Enter.
- Type 'save' to save conversation history.
- Type 'load' to load and display a conversation file.
- Type 'help' to show this help message.
- Type 'clear' to clear the screen.
- Type 'exit', 'quit', or 'stop' to exit.
""")

    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    while True:
        command = dispatcher.listen()
        if command:
            command_lower = command.strip().lower()
            if command_lower == 'save':
                save_conversation()
                continue
            if command_lower == 'load':
                load_conversation()
                continue
            if command_lower == 'help':
                show_help()
                continue
            if command_lower == 'clear':
                clear_screen()
                continue
            conversation.append(f"You: {command}")
            handled = dispatcher.handle(command)
            if handled:
                continue
            if any(exit_word in command_lower for exit_word in ["exit", "quit", "stop"]):
                tts.speak("Goodbye!")
                break

if __name__ == "__main__":
    main() 