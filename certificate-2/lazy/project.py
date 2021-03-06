"""
RoboCorp Certificate level 2

"""

from RPA.Browser.Selenium import Selenium
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF

import time
from datetime import timedelta


class Certificate:
    def __init__(self, downloading_path, screenshot_path, pdf_path, receipt_directory, csv_path):

        self.browser = Selenium()
        self.http = HTTP()
        self.table = Tables()
        self.pdf = PDF()

        self.downloading_path = downloading_path
        self.screenshot_path = screenshot_path
        self.pdf_path = pdf_path
        self.receipt_directory = receipt_directory
        self.csv_path = csv_path

    def download_directory(self):
        self.browser.set_download_directory(directory=self.downloading_path)

    def open_browser(self):
        while True:
            try:
                self.browser.open_available_browser("https://robotsparebinindustries.com/#/robot-order")
                time.sleep(1)
            except Exception as e:
                print(e)
            else:
                break

    def click_ok(self):
        self.browser.wait_until_page_contains_element(locator="//*[contains(text(), 'OK')]")
        self.browser.click_button_when_visible(locator="//*[contains(text(), 'OK')]")

    def download_orders_csv(self):
        self.http.download("https://robotsparebinindustries.com/orders.csv", overwrite=False)

    def orders(self):
        orders_data = self.table.read_table_from_csv(path=self.csv_path, header=True)
        for order in orders_data:
            print(order)
            self.browser.select_from_list_by_value("//select[@id='head']", order['Head'])
            """
            What actually is group name?
            IF there is radio button, it means it contains multiple inputs so check the name attribute
              and all inputs have same name, So we can say that is group name.
            """
            self.browser.select_radio_button(group_name="body", value=order['Body'])
            self.browser.input_text(locator="//*[contains(@placeholder, 'Enter')]", text=str(order['Legs']))
            self.browser.input_text(locator="//*[contains(@placeholder, 'address')]", text=order['Address'])
            self.browser.click_button_when_visible(locator="//*[contains(text(), 'Preview')]")
            while True:
                try:
                    self.browser.wait_until_page_contains_element(locator="(//*[contains(text(), 'Order')])[2]",
                                                                  timeout=timedelta(seconds=17))
                    self.browser.click_button_when_visible(locator="(//*[contains(text(), 'Order')])[2]")
                    self.browser.wait_until_page_contains_element(locator="//div[@id='receipt']",
                                                                  timeout=timedelta(seconds=17))

                    break
                except Exception:
                    pass
            time.sleep(1)
            self.browser.screenshot(locator="//div[@id='robot-preview-image']",
                                    filename=f"{self.screenshot_path}/{order['Order number']}.png")
            receipt_html = self.browser.get_element_attribute(locator="//div[@id='receipt']", attribute='innerHTML')
            self.pdf.html_to_pdf(receipt_html, f"{self.pdf_path}/{order['Order number']}.pdf")
            self.pdf.add_watermark_image_to_pdf(image_path=f"{self.screenshot_path}/{order['Order number']}.png",
                                                source_path=f"{self.pdf_path}/{order['Order number']}.pdf",
                                                output_path=f"{self.receipt_directory}/{order['Order number']}.pdf")
            # another order
            self.browser.click_button_when_visible(locator="//*[contains(text(), 'another')]")
            """
            Re-use the above click_ok method, advantages of using OOP
            """
            self.click_ok()

        time.sleep(5)
