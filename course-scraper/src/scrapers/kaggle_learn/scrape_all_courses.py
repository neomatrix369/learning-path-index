"""
Scrape Courses from Kaggle Learn
This script makes use of the internal Kaggle Learn API to retrieve course information
Without parsing any HTML
"""

from pathlib import Path

import requests
from config import CONFIG
from pydantic import BaseModel
from scrapers.kaggle_learn.models import (
    KaggleCourse,
)
from utils import get_safestring

KAGGLE_COURSE_API_URL = (
    "https://www.kaggle.com/api/i/education.EducationService/GetTracks"
)

KAGGLE_DATA_PATH = Path(CONFIG.DATA_PATH, "KaggleLearnCourses")
KAGGLE_DATA_PATH.mkdir(exist_ok=True)


def get_page_details(url: str) -> dict:
    """
    Get all courses and their details from Kaggle Learn Homepage https://www.kaggle.com/learn/
    """
    session = requests.Session()
    # Make a preparatory request to get relevant cookies
    session.get(url)
    xsrf_token = session.cookies.get("XSRF-TOKEN")
    r = session.post(
        KAGGLE_COURSE_API_URL,
        headers={"X-Xsrf-Token": xsrf_token, "Content-Type": "application/json"},
        json={},
    )

    return r.json()


class AllKaggleCourses(BaseModel):
    tracks: list[KaggleCourse]


page = AllKaggleCourses.parse_obj(
    get_page_details("https://www.kaggle.com/learn/feature-engineering")
)

for course in page.tracks:
    file_name = get_safestring(course.name)
    with open(
        KAGGLE_DATA_PATH.joinpath(f"{file_name}.csv"), "w", encoding="utf-8"
    ) as f:
        course.write_course_summary_to_file(f)
