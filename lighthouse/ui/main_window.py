import os
import threading
import tkinter as tk
from tkinter import messagebox

from config.settings import *
from models.lead import Lead
from services.search_service import SearchService
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
        ).pack(side="left", padx=20, pady=15)

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

        self.search_panel = SearchPanel(
            body,
            on_search=self.run_search,
        )
        self.search_panel.pack(fill="x", pady=(0, 16))

        self.dashboard = DashboardCards(
            body,
            total_leads=self.repository.count(),
        )
        self.dashboard.pack(fill="x", pady=(0, 16))

        self.table = LeadTable(
            body,
            self.repository.list_all(),
        )
        self.table.pack(fill="both", expand=True)

    def run_search(self, niche: str, country: str, limit: int):
        token = os.getenv("APIFY_TOKEN")

        if not token:
            messagebox.showerror(
                "Missing API Token",
                "APIFY_TOKEN is not set in this terminal.",
            )
            return

        self.search_panel.set_busy(True)
        self.dashboard.set_status("Searching")

        thread = threading.Thread(
            target=self._search_worker,
            args=(token, niche, country, limit),
            daemon=True,
        )
        thread.start()

    def _search_worker(
        self,
        token: str,
        niche: str,
        country: str,
        limit: int,
    ):
        try:
            service = SearchService(token)

            results = service.search(
                niche=niche,
                country=country,
                limit=limit,
            )

            added = 0

            for result in results:
                was_added = self.repository.add(
                    Lead(
                        company=result["company"],
                        website=result["website"],
                        industry=niche,
                        country=country,
                        status="New",
                    )
                )

                if was_added:
                    added += 1

            self.root.after(
                0,
                lambda: self._finish_search(
                    added=added,
                    returned=len(results),
                ),
            )

        except Exception as error:
            self.root.after(
                0,
                lambda: self._search_failed(str(error)),
            )

    def _finish_search(self, added: int, returned: int):
        self.table.refresh(self.repository.list_all())
        self.dashboard.set_total(self.repository.count())
        self.dashboard.set_status("Idle")
        self.search_panel.set_busy(False)

        messagebox.showinfo(
            "Search Complete",
            f"Returned: {returned}\n"
            f"New leads added: {added}",
        )

    def _search_failed(self, error: str):
        self.dashboard.set_status("Error")
        self.search_panel.set_busy(False)

        messagebox.showerror(
            "Search Failed",
            error,
        )

    def run(self):
        self.root.mainloop()