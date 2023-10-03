from pydantic import BaseModel
from typing import Optional


class Activity(BaseModel):
    """
    For clarity, during visualization, skip the intermediate model
    and show CourseSubmodule - Activity relationships
    """

    id: str
    href: Optional[str]
    duration: int | float
    title: str
    type: str


class CourseStep(BaseModel):
    id: str
    isOptional: bool
    activities: list[Activity]  # Usually has one activity, containing the actual title
    allActivitiesRequired: bool


class CourseSubmodule(BaseModel):
    id: str
    title: str
    description: Optional[str]
    steps: list[CourseStep]
    expanded: bool

    def __hash__(self) -> int:
        return int(self.id)


class Course(BaseModel):
    __root__: list[CourseSubmodule]  # __root__ == 🌟
