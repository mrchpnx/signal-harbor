import tkinter as tk
from tkinter import ttk

from config.settings import BACKGROUND, PRIMARY


class LeadTable:
    def __init__(self, parent: tk.Widget, leads) -> None:
        self.frame = tk.Frame(parent, bg=BACKGROUND)

        columns = (
            "company",
            "website",
            "industry",
            "country",
            "status",
        )

        self.tree = ttk.Treeview(
            self.frame,
            columns=columns,
            show="headings",
            height=18,
        )

        self.tree.heading("company", text="Company")
        self.tree.heading("website", text="Website")
        self.tree.heading("industry", text="Industry")
        self.tree.heading("country", text="Country")
        self.tree.heading("status", text="Status")

        self.tree.column("company", width=220)
        self.tree.column("website", width=280)
        self.tree.column("industry", width=170)
        self.tree.column("country", width=150)
        self.tree.column("status", width=110)

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview.Heading",
            background=PRIMARY,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
        )

        style.map(
            "Treeview.Heading",
            background=[("active", PRIMARY)],
            foreground=[("active", "white")],
        )
        style.configure(
            "Treeview",
            rowheight=30,
            font=("Segoe UI", 10),
        )

        scrollbar = ttk.Scrollbar(
            self.frame,
            orient="vertical",
            command=self.tree.yview,
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar.pack(
            side="right",
            fill="y",
        )

        self.load(leads)

    def load(self, leads) -> None:
        for lead in leads:
            self.tree.insert(
                "",
                "end",
                values=(
                    lead.company,
                    lead.website,
                    lead.industry,
                    lead.country,
                    lead.status,
                ),
            )

    def pack(self, **kwargs) -> None:
        self.frame.pack(**kwargs)