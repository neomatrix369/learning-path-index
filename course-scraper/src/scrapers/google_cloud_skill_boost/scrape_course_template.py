import csv
import io
from collections import defaultdict
from html import unescape
from pathlib import Path

import requests
from config import CONFIG
from lxml import etree
from scrapers.google_cloud_skill_boost.models import Activity, Course, CourseSubmodule
from utils import get_safestring

COURSE_CODE = "CLMML11"

DATA_FOLDER = Path(CONFIG.DATA_PATH, COURSE_CODE)
DATA_FOLDER.mkdir(exist_ok=True, parents=True)

course_modules_mapping = {}
with open(DATA_FOLDER.joinpath(f"{COURSE_CODE}-Courses.csv")) as f:
    course_meta = io.StringIO(f.read())

csvreader = csv.DictReader(course_meta)
for course in csvreader:
    # TODO: Support scraping GCB Labs
    if "labs" in course["title"].lower():
        continue
    r = requests.get(course["link"])
    print(str(r.content)[:100])
    html_parser = etree.HTMLParser()
    dom = etree.fromstring(r.content, html_parser)

    prerequisites = None
    if prerequisites := dom.xpath(
        "(//div[div/text() = 'Prerequisites'])/following-sibling::div/text()"
    ):
        prerequisites = "".join(prerequisites[0]).replace("\n", " ")

    if course_modules := dom.xpath("//ql-course/@modules"):
        course_modules = course_modules[0]
        course_modules = unescape(course_modules)
    else:
        continue

    course_modules_mapping[course["title"]] = course_modules

    with open(
        DATA_FOLDER.joinpath(f"{COURSE_CODE}-Modules-Meta.csv"),
        "a",
        encoding="utf-8",
    ) as f:
        csvwriter = csv.writer(f)
        print(prerequisites)
        csvwriter.writerow([course["title"], course["link"], prerequisites])

for course_title, course_module in course_modules_mapping.items():
    parsed_courses = [c for c in Course.parse_raw(course_module).__root__]
    submodule_activities: dict[CourseSubmodule, list[dict]] = defaultdict(list)

    # Link Submodules with their activities
    for submodule in parsed_courses:
        for step in submodule.steps:
            submodule_activities[submodule].extend(
                [activity.dict() for activity in step.activities]
            )

    course_title = get_safestring(course_title)

    for submodule in submodule_activities:
        submodule_title = get_safestring(submodule.title)
        with open(
            DATA_FOLDER.joinpath(f"{submodule_title}.csv"),
            "w",
            encoding="utf-8",
        ) as f:
            fieldnames = Activity.__fields__.keys()
            csvwriter = csv.DictWriter(f, fieldnames)
            csvwriter.writeheader()
            csvwriter.writerows(submodule_activities[submodule])

    with open(DATA_FOLDER.joinpath(f"{course_title}.csv"), "w", encoding="utf-8") as f:
        excluded_fields = {"steps", "expanded"}
        fieldnames = sorted(set(CourseSubmodule.__fields__.keys()) - excluded_fields)
        csvwriter = csv.DictWriter(f, fieldnames)
        csvwriter.writeheader()
        csvwriter.writerows(
            [submodule.dict(exclude=excluded_fields) for submodule in parsed_courses]
        )
