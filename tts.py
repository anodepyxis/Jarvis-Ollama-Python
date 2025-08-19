import pyttsx3
import threading
import queue

class TTSManager:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def speak(self, text):
        self.queue.put(text)

    def _run(self):
        while True:
            text = self.queue.get()
            if text is None:
                break
            self.engine.say(text)
            self.engine.runAndWait()

    def stop(self):
        self.queue.put(None)
        self.thread.join() 