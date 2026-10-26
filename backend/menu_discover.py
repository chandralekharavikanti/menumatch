
"""Discover and rank possible menu links from restaurant websites."""

from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup


MENU_KEYWORDS = (
    "menu",
    "food",
    "dining",
    "order",
    "nutrition",
    "allergen",
)

MAX_LINKS = 10

COMMON_MENU_PATHS = (
    "/menu",
    "/menus",
    "/food",
    "/our-menu",
    "/food-menu",
)


def menu_score(link: dict) -> int:
    """Give higher scores to links more likely to contain menus."""

    title = link["title"].lower()
    url = link["url"].lower()

    score = 0

    if "view full menu" in title:
        score += 10
    elif "menu" in title:
        score += 7

    if "menu" in url:
        score += 4

    if "nutrition" in title or "allergen" in title:
        score += 5

    if "order" in title or "/order" in url:
        score -= 3

    if any(
        word in title
        for word in ("rewards", "careers", "account", "app")
    ):
        score -= 10

    if any(
        word in url
        for word in (
            "play.google.com",
            "apps.apple.com",
            "instagram.com",
            "facebook.com",
        )
    ):
        score -= 10

    return score


def discover_menu_links(website_url: str) -> list[dict]:
    """Find and rank menu-related links on a restaurant homepage."""

    parsed = urlparse(website_url)

    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Enter a valid http or https website URL.")

    headers = {
        "User-Agent": "MenuMatch/0.1 (menu discovery prototype)"
    }

    try:
        with httpx.Client(
            timeout=15,
            follow_redirects=True,
            headers=headers,
        ) as client:
            response = client.get(website_url)
            response.raise_for_status()

    except httpx.HTTPError as exc:
        print(f"Could not retrieve website: {exc}")
        return []

    content_type = response.headers.get("content-type", "").lower()

    if "text/html" not in content_type:
        print("The website did not return an HTML page.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    found = []
    seen = set()

    for anchor in soup.find_all("a", href=True):
        link_text = anchor.get_text(" ", strip=True)
        href = anchor["href"]

        absolute_url = urljoin(str(response.url), href)
        parsed_link = urlparse(absolute_url)

        if parsed_link.scheme not in {"http", "https"}:
            continue

        searchable_text = f"{link_text} {href}".lower()

        if not any(
            keyword in searchable_text
            for keyword in MENU_KEYWORDS
        ):
            continue

        if absolute_url in seen:
            continue

        seen.add(absolute_url)

        found.append({
            "title": link_text or "Possible menu",
            "url": absolute_url,
        })

    found.sort(key=menu_score, reverse=True)

    # Discard obviously unrelated links.
    found = [
        link for link in found
        if menu_score(link) > 0
    ]

    return found[:MAX_LINKS]


def check_common_menu_paths(website_url: str) -> list[dict]:
    """Try common menu paths if homepage discovery finds nothing."""

    parsed = urlparse(website_url)

    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Enter a valid http or https website URL.")

    found = []
    seen = set()

    with httpx.Client(
        timeout=15,
        follow_redirects=True,
        headers={"User-Agent": "MenuMatch/0.1"},
    ) as client:

        for path in COMMON_MENU_PATHS:
            url = urljoin(website_url, path)

            try:
                response = client.get(url)
                response.raise_for_status()

                content_type = response.headers.get(
                    "content-type", ""
                ).lower()

                if "text/html" not in content_type:
                    continue

                soup = BeautifulSoup(
                    response.text,
                    "html.parser",
                )

                title = (
                    soup.title.get_text(" ", strip=True)
                    if soup.title
                    else ""
                )

                final_url = str(response.url)

                if final_url in seen:
                    continue

                if (
                    "menu" in title.lower()
                    or "menu" in response.url.path.lower()
                ):
                    found.append({
                        "title": title or "Possible menu",
                        "url": final_url,
                    })

                    seen.add(final_url)

            except httpx.HTTPError:
                continue

    found.sort(key=menu_score, reverse=True)

    return found[:MAX_LINKS]


if __name__ == "__main__":

    website = input(
        "Enter restaurant website URL: "
    ).strip()

    links = discover_menu_links(website)

    if not links:
        print(
            "No menu links on homepage. "
            "Checking common menu paths..."
        )

        links = check_common_menu_paths(website)

    if not links:
        print("No accessible menu pages found.")

    else:
        print(f"\nFound {len(links)} possible menu links:\n")

        for link in links:
            print(f"{link['title']} -> {link['url']}")
