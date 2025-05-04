"""
This script scrapes all courses from the DeepLearning website.
It assumes that the courses are stored in an Algolia index, and that the Alogolia API URL remains constant.
This URL will need to be updated if the Algolia index is changed.
"""

import csv
import logging
import os
from pathlib import Path
from typing import List

import requests
from config import CONFIG

from scrapers.deeplearning.models import Course, CourseIndex

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

ALGOLIA_URL = os.environ["DEEPLEARNING_AI_ALGOLIA_URL"]
# "https://y5109wlmqw-1.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.20.0)%3B%20Browser%20(lite)%3B%20instantsearch.js%20(4.75.1)%3B%20react%20(18.3.1)%3B%20react-instantsearch%20(7.13.4)%3B%20react-instantsearch-core%20(7.13.4)%3B%20next.js%20(14.2.28)%3B%20JS%20Helper%20(3.22.5)&x-algolia-api-key=9030ff79d3ba653535d5b66c26b56683&x-algolia-application-id=Y5109WLMQW"
COURSE_CODE = "DEEPAI"
DATA_FOLDER = Path(CONFIG.DATA_PATH, COURSE_CODE)
DATA_FOLDER.mkdir(exist_ok=True, parents=True)


def fetch_courses_from_algolia() -> List[dict]:
    """
    Fetch courses from the Algolia index.
    Returns a list of course dictionaries.
    """
    logger.info("Starting to fetch courses from Algolia.")
    session = requests.Session()
    nb_pages = None
    curr_page = 0
    all_results = []

    try:
        while curr_page != nb_pages:
            logger.info(f"Fetching page {curr_page} from Algolia.")
            response = session.post(
                ALGOLIA_URL,
                json={
                    "requests": [
                        {
                            "indexName": "courses_date_desc",
                            "params": f"page={curr_page}",
                        }
                    ]
                },
            )
            if response.status_code == 200:
                data = response.json()
                result = data.get("results", [])[0]
                hits = result.get("hits", [])
                all_results.extend(hits)
                if nb_pages := int(result.get("nbPages", 0)):
                    curr_page += 1
            else:
                logger.error(
                    f"Failed to fetch data from Algolia. Status code: {response.status_code} {response.text}"
                )
                break
    except Exception as error:
        logger.exception(f"Error fetching data from Algolia: {error}")
        return []

    logger.info(f"Successfully fetched {len(all_results)} courses from Algolia.")
    return all_results


def parse_algolia_data(data: list[dict]):
    """Receives and parses hits from the Algolia index."""
    logger.info("Starting to parse Algolia data.")
    courses: List[Course] = []
    course_indexes: List[CourseIndex] = []

    for hit in data:
        try:
            module_code = "DEEPAI:" + hit.get("objectID", "UNKNOWN")
            course_learning_material = hit.get("title", "UNKNOWN")
            source = "Deep Learning AI"
            course_level = (
                hit.get("skill_level", [None])[0]
                if hit.get("skill_level")
                else "Unknown"
            )
            type_free_paid = (
                "Free"
                if hit.get("course_type", "UNKNOWN") == "Short Course"
                else "Paid"
            )
            landing_page = "https://deeplearning.ai/" + hit.get("landing_page", "")
            keywords_tags = ", ".join(hit.get("topic", []))
            difficulty_level = (
                hit.get("skill_level", [None])[0] if hit.get("skill_level") else None
            )

            # Create record for Data Store 1
            course_record = Course(
                Module_Code=module_code,
                Source=source,
                Course_Level=course_level,
                Course_Learning_Material=course_learning_material,
                Course_Learning_Material_Link=landing_page,
                Type_Free_Paid=type_free_paid,
            )
            courses.append(course_record.model_dump())

            # Create record for Data Store 2
            course_index = CourseIndex(
                Module_Code=module_code,
                Course_Learning_Material=course_learning_material,
                Source=source,
                Course_Level=course_level,
                Type_Free_Paid=type_free_paid,
                Module=course_learning_material,
                Links=landing_page,
                Keywords_Tags_Skills_Interests_Categories=keywords_tags,
                Difficulty_Level=difficulty_level,
            )
            course_indexes.append(course_index.model_dump())
        except Exception as error:
            logger.exception(f"Error parsing course data: {error}")

    logger.info(
        f"Parsed {len(courses)} courses and {len(course_indexes)} course indexes."
    )
    return courses, course_indexes


if __name__ == "__main__":
    logger.info("Script started.")
    course_hits = fetch_courses_from_algolia()
    if course_hits:
        courses, course_indexes = parse_algolia_data(course_hits)
        logger.info(f"Fetched {len(course_hits)} courses from Algolia.")

        try:
            with open(
                DATA_FOLDER.joinpath(
                    f"{COURSE_CODE}-Courses_and_Learning_Materials.csv"
                ),
                "w",
                encoding="utf-8",
            ) as f:
                writer = csv.DictWriter(f, fieldnames=courses[0].keys())
                writer.writeheader()
                writer.writerows(courses)
                logger.info(
                    f"Successfully exported {len(courses)} records to {DATA_FOLDER.joinpath(f'{COURSE_CODE}-Courses_and_Learning_Materials.csv')}"
                )
        except Exception as error:
            logger.exception(f"Error writing courses to CSV: {error}")

        try:
            with open(
                DATA_FOLDER.joinpath(f"{COURSE_CODE}-Learning_Pathway_Index.csv"),
                "w",
                encoding="utf-8",
            ) as f:
                writer = csv.DictWriter(f, fieldnames=course_indexes[0].keys())
                writer.writeheader()
                writer.writerows(course_indexes)
                logger.info(
                    f"Successfully exported {len(course_indexes)} records to {DATA_FOLDER.joinpath(f'{COURSE_CODE}-Learning_Pathway_Index.csv')}"
                )
        except Exception as error:
            logger.exception(f"Error writing course indexes to CSV: {error}")
    else:
        logger.warning("No courses were fetched from Algolia.")

    logger.info("Script finished.")
