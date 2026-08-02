from dataclasses import dataclass


@dataclass
class Lead:
    company: str
    website: str
    industry: str = ""
    country: str = ""
    status: str = "New"