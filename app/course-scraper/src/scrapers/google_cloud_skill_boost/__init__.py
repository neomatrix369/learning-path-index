import re

from common import UrlScraper

URL_PATTERNS: list[re.Pattern] = []


def get_handler(url: str) -> UrlScraper | None:
    """
    Test if a URL can be scraped by a module,
    and return the corresponding handler function/class

    Args:
        url (str): URL to test/scrape
    """
    if any([pattern.match(url) for pattern in URL_PATTERNS]):
        return lambda: True
