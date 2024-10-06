from csv import DictWriter
from pathlib import Path
from urllib.parse import urljoin
from lxml import etree

from scrapers.google_cloud_skill_boost import pages
from config import CONFIG
import requests
import sys
import os

COURSE_CODE = "CLMML11"
GCSB_HOME_URL = "https://www.cloudskillsboost.google/"
GCSB_LOGIN_URL = "https://www.cloudskillsboost.google/users/sign_in"

DATA_FOLDER = Path(CONFIG.DATA_PATH, COURSE_CODE)
DATA_FOLDER.mkdir(exist_ok=True, parents=True)


# Open Journey Path
def extract_ml_learning_path(GCSB_JOURNEY_URL) -> list[dict]:
    # Send a request to the provided URL
    r = requests.get(GCSB_JOURNEY_URL)
    html_parser = etree.HTMLParser()
    dom = etree.fromstring(r.content, html_parser)

    data = []
    for journey in dom.xpath(pages.GCSBLearningJourneyPage.journeys):
        try:
            # Try to extract the first element from journey details
            details = journey.xpath(pages.GCSBLearningJourneyPage.journey_details)[0]
        except IndexError:
            # If the first element is not available, use the full result or provide a default value
            details = journey.xpath(pages.GCSBLearningJourneyPage.journey_details)
            details = details if details else "No details available"

        try:
            # Try to extract the first link and construct the full URL
            link = urljoin(GCSB_HOME_URL, journey.xpath(pages.GCSBLearningJourneyPage.journey_link)[0])
        except IndexError:
            # If the link is missing, handle it gracefully
            link = urljoin(GCSB_HOME_URL, journey.xpath(pages.GCSBLearningJourneyPage.journey_link))
            link = link if link else "No link available"

        # Append the extracted information to the data list
        data.append(
            {
                "title": journey.xpath(pages.GCSBLearningJourneyPage.journey_title)[0].strip() if journey.xpath(pages.GCSBLearningJourneyPage.journey_title) else "No title available",
                "details": details.strip(),  # Use the result from the try-except block
                "description": journey.xpath(pages.GCSBLearningJourneyPage.journey_description)[0].strip() if journey.xpath(pages.GCSBLearningJourneyPage.journey_description) else "No description available",
                "link": link,
            }
        )

    return data
if __name__ == "__main__":

    try:
        import config
        GCSB_JOURNEY_URL = CONFIG.GCSB_JOURNEY_URL  # Directly access GCSB_JOURNEY_URL
        print(f'Using this URL: {GCSB_JOURNEY_URL}')
    except (ImportError, AttributeError):
        GCSB_JOURNEY_URL = input("Enter the GCSB Journey URL: ")

    data = extract_ml_learning_path(GCSB_JOURNEY_URL)



# Check if data is not empty
if not data:
    print("No data to write!")
else:
    try:
        # Writing to the CSV file
        with open(DATA_FOLDER.joinpath(f"{COURSE_CODE}-Courses.csv"), "w", encoding="utf-8", newline='') as f:
            csvwriter = DictWriter(f, fieldnames=["title", "details", "description", "link"])
            csvwriter.writeheader()
            csvwriter.writerows(data)
        print(f"Data successfully written to {COURSE_CODE}-Courses.csv")
    except Exception as e:
        print(f"An error occurred while writing the file: {e}")
