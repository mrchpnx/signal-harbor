from database.lead_repository import LeadRepository
from models.lead import Lead
from ui.main_window import MainWindow


repository = LeadRepository()

repository.add(
    Lead(
        company="Signal Harbor Test Lead",
        website="https://example.com",
        industry="Ecommerce",
        country="United States",
    )
)

app = MainWindow(repository)

app.run()