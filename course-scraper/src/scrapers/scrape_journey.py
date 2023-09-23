from csv import DictWriter
from pathlib import Path
from urllib.parse import urljoin

import pages
from config import CONFIG
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")

# Uncomment to use your personal Chrome profile instead of incognito. (Use with caution)
# options.add_argument(f"--user-data-dir={CONFIG.CHROME_USER_DATA_DIR}")
# options.add_argument(f"--profile-directory={CONFIG.CHROME_USER}")

driver = webdriver.Chrome(options=options)
print("Web driver binary loaded successfully")


def login_to_gcb(driver: WebDriver):
    driver.get(CONFIG.GCB_LOGIN_URL)
    print(driver.title)
    driver.find_element("xpath", pages.SignInCloudBoostPage.user_email).send_keys(
        CONFIG.GCB_EMAIL
    )
    driver.find_element("xpath", pages.SignInCloudBoostPage.user_password).send_keys(
        CONFIG.GCB_PASSWORD
    )
    driver.find_element("xpath", pages.SignInCloudBoostPage.sign_in_button).click()


# Open Journey Path
def extract_ml_learning_path(driver: WebDriver) -> list[dict]:
    driver.get(CONFIG.JOURNEY_URL)
    print(driver.title)
    data = []
    for journey in driver.find_elements("xpath", pages.MLEngineerPathGCBPath.journeys):
        data.append(
            {
                "title": journey.find_element(
                    "xpath", pages.MLEngineerPathGCBPath.journey_title
                ).text,
                "details": [
                    detail.text
                    for detail in journey.find_elements(
                        "xpath", pages.MLEngineerPathGCBPath.journey_details
                    )
                ],
                "description": journey.find_element(
                    "xpath", pages.MLEngineerPathGCBPath.journey_description
                ).text,
                "link": urljoin(
                    CONFIG.GCB_HOME_URL,
                    journey.find_element(
                        "xpath", pages.MLEngineerPathGCBPath.journey_link
                    ).get_attribute("href"),
                ),
            }
        )

    return data


login_to_gcb(driver)
ml_learning_path = extract_ml_learning_path(driver)
driver.close()

DATA_FOLDER = Path(CONFIG.DATA_PATH, CONFIG.JOURNEY_CODE)
DATA_FOLDER.mkdir(exist_ok=True)
with open(
    DATA_FOLDER.joinpath(f"{CONFIG.JOURNEY_CODE}-Courses.csv"),
    "w",
) as f:
    csvwriter = DictWriter(f, fieldnames=["title", "details", "description", "link"])
    csvwriter.writeheader()
    csvwriter.writerows(ml_learning_path)


driver.close()
print("Closed driver")
