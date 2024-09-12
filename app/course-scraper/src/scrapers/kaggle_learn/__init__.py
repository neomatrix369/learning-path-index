from common import UrlScraper


def get_handler(url: str) -> UrlScraper | None:
    """
    Test if a URL can be scraped by a module,
    and return the corresponding handler function/class

    Args:
        url (str): URL to test/scrape
    """
    ...
