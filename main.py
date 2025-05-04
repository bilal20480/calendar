import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import calendar
import datetime
import json
import os
from tkinter import font

# File to store events
EVENT_FILE = "events.json"

# Predefined festivals
FESTIVALS = {
    "01-01": "New Year",
    "15-08": "Independence Day",
    "26-01": "Republic Day",
    "02-10": "Gandhi Jayanti",
    "25-12": "Christmas",
    "14-11": "Children's Day"
}

# Load events
def load_events():
    if os.path.exists(EVENT_FILE):
        with open(EVENT_FILE, "r") as f:
            return json.load(f)
    return {}

# Save events
def save_events(events):
    with open(EVENT_FILE, "w") as f:
        json.dump(events, f, indent=4)

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌟 GPT-Powered Ultra Calendar")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#0d0d0d")
        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))

        self.events = load_events()
        self.current_date = datetime.date.today()
        self.year = self.current_date.year
        self.month = self.current_date.month

        self.setup_styles()
        self.setup_ui()
        self.show_calendar()
        self.check_today_event()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Segoe UI", 12), padding=8)
        self.style.configure("Header.TLabel", font=("Segoe UI", 28, "bold"), background="#0d0d0d", foreground="#00ffcc")
        self.style.configure("Date.TLabel", font=("Segoe UI", 11), background="#1c1c1c", foreground="#ccc")

    def setup_ui(self):
        self.header_frame = tk.Frame(self.root, bg="#0d0d0d")
        self.header_frame.pack(pady=30)

        prev_btn = tk.Button(self.header_frame, text="◀", command=self.prev_month, font=("Segoe UI", 16), bg="#1a1a1a", fg="white", width=4, bd=0, relief="flat")
        prev_btn.grid(row=0, column=0)

        self.month_year_label = tk.Label(self.header_frame, text="", font=("Segoe UI", 28, "bold"), bg="#0d0d0d", fg="#00ffcc")
        self.month_year_label.grid(row=0, column=1, padx=40)

        next_btn = tk.Button(self.header_frame, text="▶", command=self.next_month, font=("Segoe UI", 16), bg="#1a1a1a", fg="white", width=4, bd=0, relief="flat")
        next_btn.grid(row=0, column=2)

        self.calendar_frame = tk.Frame(self.root, bg="#0d0d0d")
        self.calendar_frame.pack(padx=30, fill=tk.BOTH, expand=True)

    def show_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        cal = calendar.Calendar(firstweekday=6)
        self.month_year_label.config(text=f"{calendar.month_name[self.month]} {self.year}")

        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for idx, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, width=12, height=2, bg="#202020", fg="#00ffd5", font=("Segoe UI", 12, "bold"))\
                .grid(row=0, column=idx, padx=2, pady=2, sticky="nsew")

        row = 1
        for week in cal.monthdayscalendar(self.year, self.month):
            for col, day in enumerate(week):
                frame = tk.Frame(self.calendar_frame, bg="#0d0d0d")
                frame.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
                if day == 0:
                    continue

                date_key = f"{day:02d}-{self.month:02d}-{self.year}"
                month_day = f"{day:02d}-{self.month:02d}"

                bg_color = "#1a1a1a"
                fg_color = "#ffffff"
                if month_day in FESTIVALS:
                    bg_color = "#ff6f61"  # Orange for festivals
                if date_key in self.events:
                    bg_color = "#3498db"  # Blue for events
                if (day == self.current_date.day and self.month == self.current_date.month and self.year == self.current_date.year):
                    bg_color = "#27ae60"  # Green for today

                btn = tk.Button(frame, text=str(day), font=("Segoe UI", 11, "bold"),
                                bg=bg_color, fg=fg_color, width=12, height=5,
                                relief="flat", bd=0, highlightthickness=0,
                                activebackground="#333", activeforeground="white",
                                command=lambda d=day: self.add_event(d))
                btn.pack(expand=True, fill="both")
            row += 1

    def add_event(self, day):
        date_key = f"{day:02d}-{self.month:02d}-{self.year}"

        def get_event():
            event = simpledialog.askstring("📝 Add Event", f"Enter event for {date_key}:")
            if event:
                self.events[date_key] = event
                save_events(self.events)
                messagebox.showinfo("✅ Event Added", f"Event for {date_key} saved.")
                self.show_calendar()

        self.root.after(0, get_event)

    def prev_month(self):
        if self.month == 1:
            if self.year > 1900:
                self.month = 12
                self.year -= 1
        else:
            self.month -= 1
        self.show_calendar()

    def next_month(self):
        if self.month == 12:
            if self.year < 2100:
                self.month = 1
                self.year += 1
        else:
            self.month += 1
        self.show_calendar()

    def check_today_event(self):
        today = datetime.date.today()
        date_key = f"{today.day:02d}-{today.month:02d}-{today.year}"
        if date_key in self.events:
            self.root.after(1000, lambda: messagebox.showinfo("🔔 Reminder", f"Today: {self.events[date_key]}"))
        elif f"{today.day:02d}-{today.month:02d}" in FESTIVALS:
            self.root.after(1000, lambda: messagebox.showinfo("🎉 Festival", f"Today is {FESTIVALS[f'{today.day:02d}-{today.month:02d}']}!"))

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
