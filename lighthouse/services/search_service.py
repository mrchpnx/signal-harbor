from urllib.parse import urlparse

import requests


class SearchService:
    def __init__(self, token: str):
        self.token = token

    def search(
        self,
        niche: str,
        country: str,
        limit: int,
    ) -> list[dict]:
        print(
            f"Search started: niche={niche}, "
            f"country={country}, limit={limit}"
        )

        url = (
            "https://api.apify.com/v2/acts/"
            "apify~google-search-scraper/"
            "run-sync-get-dataset-items"
        )

        queries = "\n".join(
            [
                f'inurl:/products/ "{niche}" "{country}"',
                f'inurl:/collections/ "{niche}" "{country}"',
                f'"Powered by Shopify" "{niche}" "{country}"',
            ]
        )

        payload = {
            "queries": queries,
            "maxPagesPerQuery": 3,
            "resultsPerPage": 10,
        }

        response = requests.post(
            url,
            params={"token": self.token},
            json=payload,
            timeout=180,
        )

        print(f"Apify status: {response.status_code}")

        if not response.ok:
            raise RuntimeError(
                f"Apify request failed with status "
                f"{response.status_code}:\n{response.text}"
            )

        pages = response.json()
        print(f"Apify returned {len(pages)} page records")

        blocked_domains = {
            "shopify.com",
            "apps.shopify.com",
            "myshopify.com",
            "instagram.com",
            "facebook.com",
            "tiktok.com",
            "youtube.com",
            "reddit.com",
            "quora.com",
            "pinterest.com",
            "linkedin.com",
            "amazon.com",
            "wikipedia.org",
            "squareup.com",
            "omnisend.com",
            "commerce-ui.com",
            "hyghstreet.com",
            "gempages.net",
            "skailama.com",
            "eastsideco.com",
            "selfnamed.com",
            "rapidfulfillment.com",
            "ukworldwideforwarding.com",
        }

        blocked_paths = (
            "/blog/",
            "/blogs/",
            "/insights/",
            "/article/",
            "/articles/",
            "/guide/",
            "/guides/",
            "/news/",
            "/resources/",
            "/marketplace/",
            "/apps/",
        )

        blocked_titles = (
            "best shopify",
            "top shopify",
            "shopify stores examples",
            "shopify app",
            "fulfillment services",
            "fulfilment services",
            "how to",
            "guide",
            "list of",
            "marketplace",
            "platform",
        )

        results = []
        seen_domains = set()

        for page in pages:
            organic_results = page.get("organicResults", [])
            print(
                f"Organic results on page: "
                f"{len(organic_results)}"
            )

            for result in organic_results:
                result_url = result.get("url", "").strip()
                title = result.get("title", "").strip()
                company = result.get(
                    "websiteTitle", ""
                ).strip()
                description = result.get(
                    "description", ""
                ).strip()

                print("\nCANDIDATE")
                print(f"Title: {title}")
                print(f"URL: {result_url}")

                if not result_url:
                    print("SKIPPED: Missing URL")
                    continue

                parsed = urlparse(result_url)
                domain = (
                    parsed.netloc
                    .lower()
                    .removeprefix("www.")
                )

                if not domain:
                    print("SKIPPED: Invalid domain")
                    continue

                domain_is_blocked = any(
                    domain == blocked
                    or domain.endswith(f".{blocked}")
                    for blocked in blocked_domains
                )

                if domain_is_blocked:
                    print(
                        f"SKIPPED: Blocked domain: {domain}"
                    )
                    continue

                lowered_url = result_url.lower()
                lowered_title = title.lower()

                matching_path = next(
                    (
                        path
                        for path in blocked_paths
                        if path in lowered_url
                    ),
                    None,
                )

                if matching_path:
                    print(
                        "SKIPPED: Blocked path: "
                        f"{matching_path}"
                    )
                    continue

                matching_title = next(
                    (
                        fragment
                        for fragment in blocked_titles
                        if fragment in lowered_title
                    ),
                    None,
                )

                if matching_title:
                    print(
                        "SKIPPED: Blocked title: "
                        f"{matching_title}"
                    )
                    continue

                if domain in seen_domains:
                    print(
                        f"SKIPPED: Duplicate domain: {domain}"
                    )
                    continue

                seen_domains.add(domain)

                lead = {
                    "company": (
                        company
                        or domain.split(".")[0]
                        .replace("-", " ")
                        .title()
                    ),
                    "title": title,
                    "website": f"https://{domain}",
                    "description": description,
                }

                print(f"ACCEPTED: {lead['website']}")
                results.append(lead)

        final_results = results[:limit]

        print(
            f"\nFiltered results: "
            f"{len(final_results)}"
        )

        return final_results