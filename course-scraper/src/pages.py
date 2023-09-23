"""
Selectors for different HTML pages
Plural attributes imply a list of elements are returned by the xpath,
rather than a single element
"""


class SignInCloudBoostPage:
    user_email = '//input[@id="user_email"]'
    user_password = '//input[@id="user_password"]'
    sign_in_button = '//button[@data-analytics-action="clicked_sign_in"]'


class MLEngineerPathGCBPath:
    journeys = "//div[@class='activity-card']"
    journey_title = ".//h2[2]"
    journey_details = (
        ".//div[@class='activity-details']//div[contains(@class, 'ql-subhead-1')]"
    )
    journey_description = ".//p"
    journey_link = ".//ql-button[contains(text(), 'Learn more')]"


class GCBCoursePage:
    """
    Skill Boost Course page

    Should be used with requests & lxml pair. X-paths are not compatitible with selenium find_element
    """

    course_title = "//h1[@class='ql-headline-1']"
    prework = "(//div[div/text() = 'Prerequisites'])/following-sibling::div/text()"

    ...
