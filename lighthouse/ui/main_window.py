import tkinter as tk

from config.settings import *
from ui.dashboard_cards import DashboardCards
from ui.lead_table import LeadTable
from ui.search_panel import SearchPanel


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
            height=70,
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text=f"{APP_NAME}   v{VERSION}",
            bg=PRIMARY,
            fg="white",
            font=("Segoe UI", 20, "bold"),
        ).pack(
            side="left",
            padx=20,
            pady=15,
        )

        body = tk.Frame(
            self.root,
            bg=BACKGROUND,
        )
        body.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=24,
        )

        search_panel = SearchPanel(body)
        search_panel.pack(
            fill="x",
            pady=(0, 16),
        )

        total = self.repository.count()

        dashboard = DashboardCards(
            body,
            total_leads=total,
        )
        dashboard.pack(
            fill="x",
            pady=(0, 16),
        )

        leads = self.repository.list_all()

        table = LeadTable(
            body,
            leads,
        )
        table.pack(
            fill="both",
            expand=True,
        )

    def run(self):
        self.root.mainloop()