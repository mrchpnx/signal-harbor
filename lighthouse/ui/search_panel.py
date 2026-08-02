import tkinter as tk
from tkinter import ttk

from config.settings import BACKGROUND


class SearchPanel:

    def __init__(self, parent):

        self.frame = tk.LabelFrame(
            parent,
            text="Automated Lead Discovery",
            bg=BACKGROUND,
            padx=20,
            pady=15,
        )

        tk.Label(
            self.frame,
            text="Niche",
            bg=BACKGROUND,
        ).grid(row=0, column=0, sticky="w")

        self.niche = ttk.Entry(
            self.frame,
            width=30,
        )

        self.niche.grid(
            row=1,
            column=0,
            padx=(0, 20),
        )

        tk.Label(
            self.frame,
            text="Country",
            bg=BACKGROUND,
        ).grid(row=0, column=1, sticky="w")

        self.country = ttk.Entry(
            self.frame,
            width=25,
        )

        self.country.grid(
            row=1,
            column=1,
            padx=(0, 20),
        )

        tk.Label(
            self.frame,
            text="Lead Count",
            bg=BACKGROUND,
        ).grid(row=0, column=2, sticky="w")

        self.count = ttk.Spinbox(
            self.frame,
            from_=1,
            to=100,
            width=8,
        )

        self.count.set(20)

        self.count.grid(
            row=1,
            column=2,
            padx=(0, 20),
        )

        ttk.Button(
            self.frame,
            text="Run Search",
        ).grid(
            row=1,
            column=3,
        )

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)