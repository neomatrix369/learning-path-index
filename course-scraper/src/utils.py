import string

SAFECHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits + ".-"


def get_safestring(string: str):
    return "".join([c for c in string if c in SAFECHARS])


def find_element_by_xpath(dom, xpath):
    return dom.xpath(xpath)[0]


def find_elements_by_xpath(dom, xpath):
    return dom.xpath(xpath)
