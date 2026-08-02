import tkinter as tk

from config.settings import BACKGROUND, PRIMARY


class DashboardCards:
    def __init__(self, parent, total_leads: int):
        self.frame = tk.Frame(parent, bg=BACKGROUND)
        self.value_labels = {}

        cards = [
            ("Total Leads", str(total_leads)),
            ("High Priority", "0"),
            ("Ready to Contact", "0"),
            ("Engine Status", "Idle"),
        ]

        for column, (title, value) in enumerate(cards):
            card = tk.Frame(
                self.frame,
                bg="white",
                highlightbackground="#D6DFEC",
                highlightthickness=1,
                padx=18,
                pady=14,
            )
            card.grid(
                row=0,
                column=column,
                sticky="nsew",
                padx=6,
            )

            tk.Label(
                card,
                text=title,
                bg="white",
                fg=PRIMARY,
                font=("Segoe UI", 11, "bold"),
            ).pack(anchor="w")

            value_label = tk.Label(
                card,
                text=value,
                bg="white",
                fg="#2563EB",
                font=("Segoe UI", 22, "bold"),
            )
            value_label.pack(anchor="w", pady=(8, 0))

            self.value_labels[title] = value_label
            self.frame.grid_columnconfigure(column, weight=1)

    def set_total(self, total: int):
        self.value_labels["Total Leads"].configure(text=str(total))

    def set_status(self, status: str):
        self.value_labels["Engine Status"].configure(text=status)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)