import customtkinter as ctk
from datetime import datetime
import json
import os
import threading
import time
from plyer import notification

# Configuration for the UI
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

DATA_FILE = "schedule_data.json"

class TimeBlockerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("TimeBlocker - Local Scheduler")
        self.geometry("500x600")
        self.resizable(False, False)

        # State
        self.scheduled_blocks = []
        self.last_triggered_time = None
        
        self.load_data()
        self.create_widgets()
        
        # Start background time checker
        self.check_schedule()

    def create_widgets(self):
        # Header
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(pady=20, padx=20, fill="x")
        
        self.label_title = ctk.CTkLabel(self.header_frame, text="Daily Schedule", font=("Roboto", 24, "bold"))
        self.label_title.pack(pady=10)

        # Input Area
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=20, fill="x")

        self.time_entry = ctk.CTkEntry(self.input_frame, placeholder_text="HH:MM (24h)", width=100)
        self.time_entry.pack(side="left", padx=10, pady=10)

        self.desc_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Task Description (e.g. Deep Work)", width=220)
        self.desc_entry.pack(side="left", padx=10, pady=10)

        self.add_btn = ctk.CTkButton(self.input_frame, text="+", width=40, command=self.add_block)
        self.add_btn.pack(side="left", padx=10)

        # Scrollable List Area
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Your Blocks")
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.refresh_list()

    def add_block(self):
        time_str = self.time_entry.get().strip()
        desc = self.desc_entry.get().strip()

        # Basic Validation
        try:
            datetime.strptime(time_str, "%H:%M")
        except ValueError:
            self.flash_error("Invalid Time Format (Use HH:MM)")
            return

        if not desc:
            self.flash_error("Description required")
            return

        # Add to list and sort
        self.scheduled_blocks.append({"time": time_str, "desc": desc})
        self.scheduled_blocks.sort(key=lambda x: x["time"])
        
        self.save_data()
        self.refresh_list()
        
        # Clear inputs
        self.time_entry.delete(0, 'end')
        self.desc_entry.delete(0, 'end')

    def delete_block(self, index):
        del self.scheduled_blocks[index]
        self.save_data()
        self.refresh_list()

    def refresh_list(self):
        # Clear current widgets in scroll frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for idx, block in enumerate(self.scheduled_blocks):
            row = ctk.CTkFrame(self.scroll_frame)
            row.pack(fill="x", pady=5)

            time_lbl = ctk.CTkLabel(row, text=block['time'], font=("Consolas", 16, "bold"), width=80)
            time_lbl.pack(side="left", padx=10)

            desc_lbl = ctk.CTkLabel(row, text=block['desc'], anchor="w")
            desc_lbl.pack(side="left", fill="x", expand=True, padx=5)

            del_btn = ctk.CTkButton(row, text="X", width=30, fg_color="red", hover_color="#8B0000",
                                    command=lambda i=idx: self.delete_block(i))
            del_btn.pack(side="right", padx=10, pady=5)

    def flash_error(self, message):
        # A simple visual feedback via window title for error
        original_title = self.title()
        self.title(f"ERROR: {message}")
        self.after(2000, lambda: self.title(original_title))

    def save_data(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self.scheduled_blocks, f)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    self.scheduled_blocks = json.load(f)
            except:
                self.scheduled_blocks = []

    def check_schedule(self):
        """
        Runs every second to check if current time matches a block.
        """
        now = datetime.now()
        current_time_str = now.strftime("%H:%M")

        # Prevent double triggering within the same minute
        if current_time_str != self.last_triggered_time:
            for block in self.scheduled_blocks:
                if block['time'] == current_time_str:
                    self.trigger_notification(block['desc'])
                    self.last_triggered_time = current_time_str
                    break 

        # Schedule next check in 1000ms (1 second)
        self.after(1000, self.check_schedule)

    def trigger_notification(self, task_desc):
        # Send Windows Toast Notification
        notification.notify(
            title='TimeBlocker Alert',
            message=f"It is time for: {task_desc}",
            app_name='TimeBlocker',
            timeout=10
        )
        
        # Bring window to front
        self.deiconify()
        self.lift()
        self.attributes('-topmost', True)
        self.after_idle(self.attributes, '-topmost', False)

if __name__ == "__main__":
    app = TimeBlockerApp()
    app.mainloop()
