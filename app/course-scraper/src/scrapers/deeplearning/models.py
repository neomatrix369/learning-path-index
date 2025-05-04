import json
from typing import List, Optional
from pydantic import BaseModel

class Course(BaseModel):
    Module_Code: str
    Source: str
    Course_Level: Optional[str] = None
    Duration: Optional[str] = None
    Prerequisites: Optional[str] = None
    Prework: Optional[str] = None
    Course_Learning_Material: str
    Course_Learning_Material_Link: str
    Type_Free_Paid: str

class CourseIndex(BaseModel):
    Module_Code: str
    Course_Learning_Material: str
    Source: str
    Course_Level: str
    Type_Free_Paid: str
    Module: str
    Duration: Optional[float] = None
    Difficulty_Level: Optional[str] = None
    Keywords_Tags_Skills_Interests_Categories: Optional[str] = None
    Links: str


