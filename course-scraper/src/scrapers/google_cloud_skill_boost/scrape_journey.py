from csv import DictWriter
from pathlib import Path
from urllib.parse import urljoin
from lxml import etree

from scrapers.google_cloud_skill_boost import pages
from config import CONFIG
import requests

COURSE_CODE = "CLMML11"
GCSB_JOURNEY_URL = "https://www.cloudskillsboost.google/journeys/118"

DATA_FOLDER = Path(CONFIG.DATA_PATH, COURSE_CODE)
DATA_FOLDER.mkdir(exist_ok=True)


# Open Journey Path
def extract_ml_learning_path() -> list[dict]:
    r = requests.get(GCSB_JOURNEY_URL)
    html_parser = etree.HTMLParser()
    dom = etree.fromstring(r.content, html_parser)

    data = []
    for journey in dom.xpath(pages.GCSBLearningJourneyPage.journeys):
        data.append(
            {
                "title": journey.xpath(pages.GCSBLearningJourneyPage.journey_title),
                "details": journey.xpath(pages.GCSBLearningJourneyPage.journey_details),
                "description": journey.xpath(
                    pages.GCSBLearningJourneyPage.journey_description
                ),
                "link": urljoin(
                    CONFIG.GCSB_HOME_URL,
                    journey.xpath(pages.GCSBLearningJourneyPage.journey_link),
                ),
            }
        )

    return data


ml_learning_path = extract_ml_learning_path()

with open(
    DATA_FOLDER.joinpath(f"{COURSE_CODE}-Courses.csv"),
    "w",
) as f:
    csvwriter = DictWriter(f, fieldnames=["title", "details", "description", "link"])
    csvwriter.writeheader()
    csvwriter.writerows(ml_learning_path)
