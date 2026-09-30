from urllib.parse import quote_plus

PLATFORM_BASES = {
    "Amazon": "https://www.amazon.in/s?k={query}",
    "Flipkart": "https://www.flipkart.com/search?q={query}",
    "IKEA": "https://www.ikea.com/in/en/search/?q={query}",
    "Swiggy": "https://www.swiggy.com/search?query={query}",
    "Zomato": "https://www.zomato.com/search?q={query}",
    "OYO": "https://www.oyorooms.com/search?q={query}",
}

def platform_url(platform: str, query: str) -> str:
    base = PLATFORM_BASES.get(platform, "https://www.google.com/search?q={query}")
    return base.format(query=quote_plus(query))

def add_links(result: dict) -> dict:
    for section in result.get("sections", []):
        for item in section.get("items", []):
            item["url"] = platform_url(
                item.get("platform", "Amazon"),
                item.get("search_query") or item.get("name", ""),
            )
    return result
