import click

from scrapers import google_cloud_skill_boost, kaggle_learn

SCRAPERS = [google_cloud_skill_boost, kaggle_learn]


@click.command()
@click.argument("url")
@click.option("--count", default=1, help="number of greetings")
def main(url=None, count=1):
    handler = None
    for scraper_module in SCRAPERS:
        if handler := scraper_module.get_handler(url):
            break
    if not handler:
        raise Exception("Could not find a suitable scraper for %s" % (url,))

    click.echo(f"Scraping: {url=} with {handler=}")


if __name__ == "__main__":
    main()
