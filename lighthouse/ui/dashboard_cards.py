import tkinter as tk

from config.settings import BACKGROUND, PRIMARY


class DashboardCards:
    def __init__(self, parent, total_leads: int) -> None:
        self.frame = tk.Frame(parent, bg=BACKGROUND)

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

            tk.Label(
                card,
                text=value,
                bg="white",
                fg="#2563EB",
                font=("Segoe UI", 22, "bold"),
            ).pack(anchor="w", pady=(8, 0))

            self.frame.grid_columnconfigure(column, weight=1)

    def pack(self, **kwargs) -> None:
        self.frame.pack(**kwargs)