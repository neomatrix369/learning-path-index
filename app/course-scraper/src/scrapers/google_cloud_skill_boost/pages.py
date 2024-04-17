"""
Selectors for different HTML pages
Plural attributes imply a list of elements are returned by the xpath,
rather than a single element
"""


# NOTE: GCSB = Google Cloud Skill Boost
class GCSBSignInPage:
    user_email = '//input[@id="user_email"]'
    user_password = '//input[@id="user_password"]'
    sign_in_button = '//button[@data-analytics-action="clicked_sign_in"]'


class GCSBLearningJourneyPage:
    """
    E.g https://www.cloudskillsboost.google/journeys/183)
    """
    learning_plan_title = "//h1[@class='learning-plan-title']/text()"
    journeys = "//div[@class='activity-card']"
    journey_title = ".//h2[2]/text()"
    journey_details = ".//div[@class='activity-details']//div[contains(@class, 'ql-title-medium')]/text()"
    journey_description = ".//p/text()"
    journey_link = ".//ql-button/@href"


class GCSBCourseTemplatePage:
    """
    Skill Boost Course page
    E.g https://www.cloudskillsboost.google/course_templates/541
    """

    course_title = "//h1[@class='ql-headline-1']"
    prework = "(//div[div/text() = 'Prerequisites'])/following-sibling::div/text()"


class GCSBFocusPage:
    """
    E.g https://www.cloudskillsboost.google/focuses/71938?parent=catalog
    """

    ...
