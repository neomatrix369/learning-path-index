"""
Scrape Courses from Kaggle Learn
This script makes use of the internal Kaggle Learn API to retrieve course information
Without parsing any HTML
"""

from pathlib import Path

import requests
from config import CONFIG
from scrapers.kaggle_learn.models import KaggleCourse

KAGGLE_COURSE_API_URL = (
    "https://www.kaggle.com/api/i/education.EducationService/GetTrack"
)

KAGGLE_DATA_PATH = Path(CONFIG.DATA_PATH, "KaggleLearnCourses")


def get_course_details(url: str) -> dict:
    """
    Get details of a Kaggle Learn course
    e.g https://www.kaggle.com/learn/feature-engineering
    """
    session = requests.Session()
    # Make a preparatory request to get relevant cookies
    session.get(url)
    xsrf_token = session.cookies.get("XSRF-TOKEN")
    track_slug = url.split("/")[-1]
    r = session.post(
        KAGGLE_COURSE_API_URL,
        headers={"X-Xsrf-Token": xsrf_token, "Content-Type": "application/json"},
        json={"trackSlug": track_slug},
    )

    return r.json()


course = KaggleCourse.parse_obj(
    get_course_details("https://www.kaggle.com/learn/feature-engineering")
)

with open(
    KAGGLE_DATA_PATH.joinpath("feature-engineering-course.csv"), "w", encoding="utf-8"
) as f:
    course.write_course_summary_to_file(f)
