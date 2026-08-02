import tkinter as tk
from config.settings import *


class MainWindow:

    def __init__(self, repository):

        self.repository = repository

        self.root = tk.Tk()

        self.root.title(APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BACKGROUND)

        self.build()

    def build(self):

        header = tk.Frame(
            self.root,
            bg=PRIMARY,
            height=70
        )

        header.pack(fill="x")

        tk.Label(
            header,
            text=f"{APP_NAME}   v{VERSION}",
            bg=PRIMARY,
            fg="white",
            font=("Segoe UI",20,"bold")
        ).pack(side="left",padx=20,pady=15)

        body = tk.Frame(
            self.root,
            bg=BACKGROUND
        )

        body.pack(fill="both", expand=True)

        total = self.repository.count()

        tk.Label(
            body,
            text=f"Total Leads: {total}",
            bg=BACKGROUND,
            fg=TEXT,
            font=("Segoe UI",28,"bold")
        ).pack(pady=80)

    def run(self):

        self.root.mainloop()