import re

todos = []

def handle_todo_command(command, tts, config):
    if command.startswith("add todo "):
        match = re.match(r'add todo (.+)', command)
        if match:
            item = match.group(1).strip()
            todos.append(item)
            tts.speak(f"Added to your todo list: {item}")
            return True
    if command == "list todos":
        if not todos:
            tts.speak("Your todo list is empty.")
        else:
            tts.speak("Here are your todos:")
            for i, item in enumerate(todos, 1):
                tts.speak(f"{i}: {item}")
        return True
    if command.startswith("remove todo "):
        match = re.match(r'remove todo (\d+)', command)
        if match:
            idx = int(match.group(1)) - 1
            if 0 <= idx < len(todos):
                removed = todos.pop(idx)
                tts.speak(f"Removed todo: {removed}")
            else:
                tts.speak("That todo number does not exist.")
            return True
    return False 