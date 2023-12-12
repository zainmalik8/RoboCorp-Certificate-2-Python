"""

X-paths

"""


class XpathMapper:
    pop_up_btn = "//*[contains(text(), 'OK')]"

    error_locator = "//div[@class='alert alert-danger']"

    head_locator = "//select[@id='head']"
    legs_input = "//*[contains(@placeholder, 'Enter')]"
    address_input = "//*[contains(@placeholder, 'address')]"
    preview_locator = "//*[contains(text(), 'Preview')]"
    order_btn = "//button[@id='order']"
    receipt_locator = "//div[@id='receipt']"
    image_locator = "//div[@id='robot-preview-image']"
    another_btn = "//*[contains(text(), 'another')]"
