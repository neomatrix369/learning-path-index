import string

SAFECHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits + ".-"


def get_safestring(string: str):
    return "".join([c for c in string if c in SAFECHARS])


def find_element_by_xpath(dom, xpath):
    return dom.xpath(xpath)[0]


def find_elements_by_xpath(dom, xpath):
    return dom.xpath(xpath)


def login_selenium_driver_to_gcb(driver: "WebDriver"):
    from scrapers.google_cloud_skill_boost import pages

    driver.get(CONFIG.GCB_LOGIN_URL)
    print(driver.title)
    driver.find_element("xpath", pages.GCSBSignInPage.user_email).send_keys(
        CONFIG.GCB_EMAIL
    )
    driver.find_element("xpath", pages.GCSBSignInPage.user_password).send_keys(
        CONFIG.GCB_PASSWORD
    )
    driver.find_element("xpath", pages.GCSBSignInPage.sign_in_button).click()
