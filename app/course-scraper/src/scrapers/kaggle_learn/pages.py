"""
Selectors for different HTML pages
Plural attributes imply a list of elements are returned by the xpath,
rather than a single element
"""


class KaggleLearnCourseListPage:
    """
    Page found at https://www.kaggle.com/learn
    """

    courses = "//section[@data-testid='course-catalog']//li[@role='listitem']"
    course_link = "//a/@href"
    course_description = "//span/text()"
    course_title = "//span/preceding-sibling::div/text()"


class KaggleLearnCourseDetailPage:
    """
    E.g https://www.kaggle.com/learn/intro-to-programming
    """

    ...
