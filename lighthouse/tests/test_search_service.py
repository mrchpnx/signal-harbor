import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.search_service import SearchService


token = os.getenv("APIFY_TOKEN")

if not token:
    raise RuntimeError("APIFY_TOKEN is not set.")

service = SearchService(token)

results = service.search(
    niche="Shopify beauty brands",
    country="United States",
    limit=5,
)

print(f"Results returned: {len(results)}")

for result in results:
    print(result)