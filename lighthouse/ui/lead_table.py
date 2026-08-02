import tkinter as tk
from tkinter import ttk

from config.settings import BACKGROUND, PRIMARY


class LeadTable:
    def __init__(self, parent, leads):
        self.frame = tk.Frame(parent, bg=BACKGROUND)

        columns = (
            "company",
            "website",
            "industry",
            "country",
            "status",
        )

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview.Heading",
            background=PRIMARY,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
        )

        style.configure(
            "Treeview",
            rowheight=30,
            font=("Segoe UI", 10),
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

        scrollbar = ttk.Scrollbar(
            self.frame,
            orient="vertical",
            command=self.tree.yview,
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refresh(leads)

    def refresh(self, leads):
        for item in self.tree.get_children():
            self.tree.delete(item)

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

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)