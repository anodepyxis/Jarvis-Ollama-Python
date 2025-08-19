import os
import shutil
import re

def handle_file_command(command, tts, config):
    if command.startswith("list files"):
        parts = command.split()
        directory = parts[2] if len(parts) > 2 else "."
        try:
            files = os.listdir(directory)
            if not files:
                tts.speak(f"No files found in {directory}.")
            else:
                tts.speak(f"Files in {directory}:")
                for f in files[:10]:
                    tts.speak(f)
        except Exception:
            tts.speak("Sorry, I couldn't list the files.")
        return True
    if command.startswith("copy file "):
        match = re.match(r'copy file (\S+) to (\S+)', command)
        if match:
            src, dst = match.group(1), match.group(2)
            try:
                shutil.copy2(src, dst)
                tts.speak(f"Copied {src} to {dst}.")
            except Exception:
                tts.speak("Sorry, I couldn't copy the file.")
            return True
    if command.startswith("move file "):
        match = re.match(r'move file (\S+) to (\S+)', command)
        if match:
            src, dst = match.group(1), match.group(2)
            try:
                shutil.move(src, dst)
                tts.speak(f"Moved {src} to {dst}.")
            except Exception:
                tts.speak("Sorry, I couldn't move the file.")
            return True
    if command.startswith("delete file "):
        match = re.match(r'delete file (\S+)', command)
        if match:
            target = match.group(1)
            try:
                os.remove(target)
                tts.speak(f"Deleted {target}.")
            except Exception:
                tts.speak("Sorry, I couldn't delete the file.")
            return True
    if command.startswith("rename file "):
        match = re.match(r'rename file (\S+) to (\S+)', command)
        if match:
            src, dst = match.group(1), match.group(2)
            try:
                os.rename(src, dst)
                tts.speak(f"Renamed {src} to {dst}.")
            except Exception:
                tts.speak("Sorry, I couldn't rename the file.")
            return True
    if command.startswith("search files for "):
        match = re.match(r'search files for (\S+)( in (\S+))?', command)
        if match:
            name = match.group(1)
            directory = match.group(3) if match.group(3) else "."
            matches = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if name.lower() in file.lower():
                        matches.append(os.path.join(root, file))
            if matches:
                tts.speak(f"Found {len(matches)} files:")
                for m in matches[:10]:
                    tts.speak(m)
            else:
                tts.speak("No files found matching that name.")
            return True
    return False 