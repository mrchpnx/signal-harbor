from database.lead_repository import LeadRepository
from ui.main_window import MainWindow


if __name__ == "__main__":
    repository = LeadRepository()
    app = MainWindow(repository)
    app.run()