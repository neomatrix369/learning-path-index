from csv import DictWriter
from pathlib import Path
from urllib.parse import urljoin
from lxml import etree

from scrapers.google_cloud_skill_boost import pages
from utils import get_safestring
from config import CONFIG
import requests

# COURSE_CODE = "CLMML11"
GCSB_JOURNEY_URL = "https://www.cloudskillsboost.google/journeys/17"
GCSB_HOME_URL = "https://www.cloudskillsboost.google/"
GCSB_LOGIN_URL = "https://www.cloudskillsboost.google/users/sign_in"

DATA_FOLDER = Path(CONFIG.DATA_PATH)
DATA_FOLDER.mkdir(exist_ok=True, parents=True)


# Open Journey Path
def extract_ml_learning_path() -> list[dict]:
    r = requests.get(GCSB_JOURNEY_URL, allow_redirects=True)
    html_parser = etree.HTMLParser()
    dom = etree.fromstring(r.content, html_parser)

    course_name = get_safestring(dom.xpath(pages.GCSBLearningJourneyPage.learning_plan_title)[0])

    data = []
    for journey in dom.xpath(pages.GCSBLearningJourneyPage.journeys):
        data.append(
            {
                "title": journey.xpath(pages.GCSBLearningJourneyPage.journey_title)[0],
                "details": journey.xpath(pages.GCSBLearningJourneyPage.journey_details)[
                    0
                ],
                "description": journey.xpath(
                    pages.GCSBLearningJourneyPage.journey_description
                )[0],
                "link": urljoin(
                    GCSB_HOME_URL,
                    journey.xpath(pages.GCSBLearningJourneyPage.journey_link)[0],
                ),
            }
        )

    return course_name, data


course_name, ml_learning_path = extract_ml_learning_path()

with open(DATA_FOLDER.joinpath(f"{course_name}.csv"), "w", encoding="utf-8") as f:
    csvwriter = DictWriter(f, fieldnames=["title", "details", "description", "link"])
    csvwriter.writeheader()
    csvwriter.writerows(ml_learning_path)
