import tkinter as tk
from tkinter import scrolledtext, Menu
import threading
from JARVIS.config import load_config
from JARVIS.tts import TTSManager
from JARVIS.dispatcher import CommandDispatcher
from JARVIS.skills import load_skills

# Theme definitions
THEMES = {
    'light': {
        'bg': '#f5f5f5', 'fg': '#222', 'input_bg': '#fff', 'input_fg': '#222',
        'text_bg': '#fff', 'text_fg': '#222', 'button_bg': '#e0e0e0', 'button_fg': '#222',
        'status_bg': '#e0e0e0', 'status_fg': '#222',
    },
    'dark': {
        'bg': '#23272e', 'fg': '#f5f5f5', 'input_bg': '#2c313c', 'input_fg': '#f5f5f5',
        'text_bg': '#181a1b', 'text_fg': '#f5f5f5', 'button_bg': '#444b5a', 'button_fg': '#f5f5f5',
        'status_bg': '#444b5a', 'status_fg': '#f5f5f5',
    }
}

def run_in_thread(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True).start()
    return wrapper

class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JARVIS Assistant")
        self.root.geometry("650x550")
        self.config = load_config()
        self.tts = TTSManager()
        self.skills = load_skills()
        self.dispatcher = CommandDispatcher(self.tts, self.config, self.skills)
        self.theme = 'dark'
        self.command_history = []
        self.history_index = None
        self._build_widgets()
        self._apply_theme()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _build_widgets(self):
        # Title label
        self.title_label = tk.Label(self.root, text="Jarvis your friend", font=("Segoe UI", 20, "bold"))
        self.title_label.pack(pady=(10, 0))
        # Menu bar
        menubar = Menu(self.root)
        theme_menu = Menu(menubar, tearoff=0)
        theme_menu.add_command(label="Light", command=lambda: self.set_theme('light'))
        theme_menu.add_command(label="Dark", command=lambda: self.set_theme('dark'))
        menubar.add_cascade(label="Theme", menu=theme_menu)
        menubar.add_command(label="Save Conversation", command=self.save_conversation)
        menubar.add_command(label="Load Conversation", command=self.load_conversation)
        menubar.add_command(label="Clear", command=self.clear_conversation)
        menubar.add_command(label="Help", command=self.show_help)
        menubar.add_command(label="About", command=self.show_about)
        menubar.add_command(label="Exit", command=self.on_close)
        self.root.config(menu=menubar)

        # Conversation area
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', font=("Consolas", 12), cursor="arrow")
        self.text_area.pack(padx=10, pady=(10,0), fill=tk.BOTH, expand=True)
        self.text_area.bind('<Button-1>', self.on_text_click)

        # Input area
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X, padx=10, pady=5)
        self.entry = tk.Entry(frame, font=("Consolas", 12))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry.bind('<Return>', lambda e: self.send_command())
        self.entry.bind('<Up>', self.history_up)
        self.entry.bind('<Down>', self.history_down)
        self.root.bind_all('<Control-l>', lambda e: self.clear_conversation())
        send_btn = tk.Button(frame, text="Send", command=self.send_command)
        send_btn.pack(side=tk.LEFT)
        speak_btn = tk.Button(frame, text="Speak", command=self.speak_command)
        speak_btn.pack(side=tk.LEFT, padx=(5, 0))
        theme_btn = tk.Button(frame, text="🌗", command=self.toggle_theme)
        theme_btn.pack(side=tk.LEFT, padx=(5, 0))

        # Status bar
        self.status = tk.Label(self.root, text="Ready", anchor='w', font=("Consolas", 10))
        self.status.pack(fill=tk.X, padx=10, pady=(0,5))

    def save_conversation(self):
        from tkinter import filedialog, messagebox
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return
        try:
            content = self.text_area.get(1.0, tk.END)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Save Conversation", "Conversation saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    def load_conversation(self):
        from tkinter import filedialog, messagebox
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.text_area.config(state='normal')
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, content)
            self.text_area.config(state='disabled')
            messagebox.showinfo("Load Conversation", "Conversation loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load: {e}")

    def show_help(self):
        from tkinter import messagebox
        help_text = (
            "JARVIS Assistant Help\n\n"
            "- Type your command and press Enter or click Send.\n"
            "- Click Speak to use voice input.\n"
            "- Use the Theme menu or 🌗 button to switch themes.\n"
            "- Ctrl+L: Clear conversation.\n"
            "- Save/Load: Save or load conversation history.\n"
            "- Click a previous command to re-run it.\n"
            "\nAvailable commands depend on your installed skills."
        )
        messagebox.showinfo("Help", help_text)

    def _apply_theme(self):
        t = THEMES[self.theme]
        self.root.configure(bg=t['bg'])
        self.text_area.configure(bg=t['text_bg'], fg=t['text_fg'], insertbackground=t['fg'])
        self.entry.configure(bg=t['input_bg'], fg=t['input_fg'], insertbackground=t['input_fg'])
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button) or isinstance(widget, tk.Label):
                widget.configure(bg=t['button_bg'], fg=t['button_fg'])
        self.status.configure(bg=t['status_bg'], fg=t['status_fg'])
        self.title_label.configure(bg=t['bg'], fg=t['fg'])

    def set_theme(self, theme):
        self.theme = theme
        self._apply_theme()

    def toggle_theme(self):
        self.theme = 'light' if self.theme == 'dark' else 'dark'
        self._apply_theme()

    def append_text(self, text, sender="You"):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, f"{sender}: {text}\n")
        self.text_area.see(tk.END)
        self.text_area.config(state='disabled')

    def clear_conversation(self):
        self.text_area.config(state='normal')
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state='disabled')

    def show_about(self):
        from tkinter import messagebox
        messagebox.showinfo("About JARVIS", "JARVIS Assistant\nModular Python AI with GUI\nby OpenAI GPT-4")

    @run_in_thread
    def send_command(self):
        command = self.entry.get().strip()
        if not command:
            return
        self.append_text(command, sender="You")
        self.command_history.append(command)
        self.history_index = None
        self.entry.delete(0, tk.END)
        self.set_status("Processing...")
        try:
            self.handle_command(command)
        except Exception as e:
            self.append_text(f"Error: {e}", sender="JARVIS")
        self.set_status("Ready")

    @run_in_thread
    def speak_command(self):
        self.set_status("Listening...")
        self.append_text("Listening...", sender="JARVIS")
        command = self.dispatcher.listen()
        if command:
            self.append_text(command, sender="You")
            self.command_history.append(command)
            self.history_index = None
            self.handle_command(command)
        else:
            self.append_text("Sorry, I did not catch that.", sender="JARVIS")
        self.set_status("Ready")

    def handle_command(self, command):
        responded = self.dispatcher.handle(command)
        if not responded:
            self.append_text("Sorry, I didn't understand that.", sender="JARVIS")
        # TTS responses are handled by TTSManager

    def set_status(self, text):
        self.status.config(text=text)

    def on_close(self):
        self.tts.stop()
        self.root.destroy()

    def history_up(self, event):
        if not self.command_history:
            return
        if self.history_index is None:
            self.history_index = len(self.command_history) - 1
        elif self.history_index > 0:
            self.history_index -= 1
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.command_history[self.history_index])

    def history_down(self, event):
        if not self.command_history or self.history_index is None:
            return
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.command_history[self.history_index])
        else:
            self.entry.delete(0, tk.END)
            self.history_index = None

    def on_text_click(self, event):
        # Allow clicking a previous command to re-run it
        index = self.text_area.index(f"@{event.x},{event.y}")
        line = self.text_area.get(f"{index} linestart", f"{index} lineend").strip()
        if line.startswith("You: "):
            command = line[5:]
            self.entry.delete(0, tk.END)
            self.entry.insert(0, command)

if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisGUI(root)
    app.append_text("Hello, I am your assistant. How can I help you?", sender="JARVIS")
    root.mainloop()