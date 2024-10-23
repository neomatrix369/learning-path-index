import argparse
import csv
import os
from csv import DictWriter
from pathlib import Path
from urllib.parse import urljoin

import requests
from config import CONFIG
from lxml import etree
from scrapers.google_cloud_skill_boost import pages

COURSE_CODE = 'CLMML11'
GCSB_HOME_URL = 'https://www.cloudskillsboost.google/'
GCSB_LOGIN_URL = 'https://www.cloudskillsboost.google/users/sign_in'

DATA_FOLDER = Path(CONFIG.DATA_PATH, COURSE_CODE)
DATA_FOLDER.mkdir(exist_ok=True, parents=True)


# Open Journey Path
def extract_ml_learning_path(GCSB_JOURNEY_URL) -> list[dict]:
    r = requests.get(GCSB_JOURNEY_URL)
    dom = etree.fromstring(r.content, etree.HTMLParser())

    data = []
    for journey in dom.xpath(pages.GCSBLearningJourneyPage.journeys):
        details = journey.xpath(pages.GCSBLearningJourneyPage.journey_details)
        details = details[0] if details else 'No details available'

        link = journey.xpath(pages.GCSBLearningJourneyPage.journey_link)
        link = urljoin(GCSB_HOME_URL, link[0]) if link else 'No link available'

        data.append(
            {
                'title': journey.xpath(pages.GCSBLearningJourneyPage.journey_title)[
                    0
                ].strip()
                if journey.xpath(pages.GCSBLearningJourneyPage.journey_title)
                else 'No title available',
                'details': details.strip(),
                'description': journey.xpath(
                    pages.GCSBLearningJourneyPage.journey_description
                )[0].strip()
                if journey.xpath(pages.GCSBLearningJourneyPage.journey_description)
                else 'No description available',
                'link': link,
            }
        )

    return data


parser = argparse.ArgumentParser(description='Extract ML learning path')
parser.add_argument('--url', help='GCSB Journey URL')
args = parser.parse_args()

GCSB_JOURNEY_URL = (
    args.url
    or os.getenv('GCSB_JOURNEY_URL')
    or CONFIG.GCSB_JOURNEY_URL
    or input('Please enter the GCSB Journey URL: ')
)

data = extract_ml_learning_path(GCSB_JOURNEY_URL)

if data:
    try:
        with open(
            DATA_FOLDER.joinpath(f'{COURSE_CODE}-Courses.csv'),
            'w',
            encoding='utf-8',
            newline='',
        ) as f:
            DictWriter(
                f, fieldnames=['title', 'details', 'description', 'link']
            ).writerows(data)
        print(f'Data successfully written to {COURSE_CODE}-Courses.csv')
    except IOError as e:
        print(f'An I/O error occurred while writing the file: {e}')
    except csv.Error as e:
        print(f'A CSV-related error occurred: {e}')
    except Exception as e:
        print(f'An unexpected error occurred while writing the file: {e}')
else:
    print('No data to write!')
