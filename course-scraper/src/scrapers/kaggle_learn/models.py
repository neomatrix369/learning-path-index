from csv import writer
from typing import Optional
from urllib.parse import urljoin

from pydantic import BaseModel, validator

KAGGLE_LEARN_URL = "https://www.kaggle.com/learn/"
KAGGLE_URL = "https://www.kaggle.com"

EMPTY_CSV_ROW = []


def convert_relative_url_to_absolute(
    relative_url: str, domain: str = KAGGLE_LEARN_URL
) -> str:
    return urljoin(domain, relative_url)


class KaggleLesson(BaseModel):
    class KaggleTutorial(BaseModel):
        name: str
        url: str  # E.g "/code/ryanholbrook/what-is-feature-engineering"
        authorUsername: str

        @validator("url", each_item=True)
        def convert_to_absolute_url(cls, url):
            return convert_relative_url_to_absolute(url, domain=KAGGLE_URL)

    description: str
    learnTutorial: KaggleTutorial


class KagglePrerequsite(BaseModel):
    name: str
    trackSlug: str

    @validator("trackSlug", each_item=True)
    def convert_to_absolute_url(cls, trackSlug):
        return convert_relative_url_to_absolute(trackSlug, domain=KAGGLE_LEARN_URL)


class KaggleAuthor(BaseModel):
    displayName: str
    userName: str


class KaggleCourse(BaseModel):
    name: str
    description: str
    estimatedTimeHours: int
    trackSlug: str
    lessons: list[KaggleLesson]
    prerequisites: Optional[list[KagglePrerequsite]]
    authors: list[KaggleAuthor]

    @validator("trackSlug", each_item=True)
    def convert_to_absolute_url(cls, trackSlug):
        return convert_relative_url_to_absolute(trackSlug, domain=KAGGLE_LEARN_URL)

    @property
    def processed_authors(self):
        return ",".join(
            [f"{author.userName}|{author.displayName}" for author in self.authors]
        )

    def write_course_summary_to_file(self, f):
        csvwriter = writer(f)
        csvwriter.writerows(
            [
                ["name", "description", "duration", "url", "authors"],
                [
                    self.name,
                    self.description,
                    self.estimatedTimeHours,
                    self.trackSlug,
                    self.processed_authors,
                ],
                EMPTY_CSV_ROW,
            ]
        )

        if self.prerequisites:
            # Write prerequisites
            csvwriter.writerow(
                ["prerequisites"],
            )
            csvwriter.writerows(
                [[p.name, p.trackSlug] for p in self.prerequisites] + EMPTY_CSV_ROW
            )

        # Write lessons
        csvwriter.writerow(["lessons"])
        csvwriter.writerow(["name", "description", "url", "authorUserName"])
        csvwriter.writerows(
            [
                [
                    lesson.learnTutorial.name,
                    lesson.description,
                    lesson.learnTutorial.url,
                    lesson.learnTutorial.authorUsername,
                ]
                for lesson in self.lessons
            ]
        )
        csvwriter.writerow(EMPTY_CSV_ROW)
