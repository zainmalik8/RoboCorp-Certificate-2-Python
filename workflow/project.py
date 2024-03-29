"""
RoboCorp Certificate level 2

"""

from datetime import timedelta

from RPA.Browser.Selenium import Selenium
from RPA.HTTP import HTTP
from RPA.PDF import PDF
from RPA.Tables import Tables, Table
from retry import retry

from config import Directories
from logger import logger
from workflow.mappers import XpathMapper


class Process(XpathMapper):
    def __init__(self):
        logger.info("Initializing the process.")

        self.browser: Selenium = Selenium()
        self.http, self.table, self.pdf = HTTP(), Tables(), PDF()

        self.csv_path = Directories.orders_path
        self.pdf_path, self.receipt_directory = Directories.pdf_directory, Directories.receipt_directory
        self.downloading_path, self.screenshot_path = Directories.output_path, Directories.screenshot_directory

        self.orders_data, self.processed_orders = Table(), 0

    def open_browser(self):
        logger.info("opening the browser.")
        self.browser.open_available_browser("https://robotsparebinindustries.com/#/robot-order", maximized=True)

    @retry(tries=3, delay=1)
    def handle_pop_up(self):
        logger.info("handling the pop-up.")
        self.browser.wait_until_page_contains_element(self.pop_up_btn, timeout=timedelta(seconds=15))
        self.browser.click_button_when_visible(self.pop_up_btn)
        return True

    def download_orders_csv(self):
        logger.info("downloading the orders csv.....")
        self.http.download("https://robotsparebinindustries.com/orders.csv", overwrite=False,
                           target_file=self.csv_path)

    @retry(tries=3, delay=1)
    def click_on_locator(self, locator: str, timeout: int = 10):
        self.browser.wait_until_page_contains_element(locator, timeout=timedelta(seconds=timeout))
        self.browser.click_element_when_visible(locator)

    def find_locator(self, locator: str, timeout: int = 10):
        try:
            self.browser.wait_until_page_contains_element(locator, timeout=timedelta(seconds=timeout))
            return self.browser.find_element(locator)
        except AssertionError:
            return

    def orders_processing(self):
        logger.info("started processing the orders.")
        self.orders_data = self.table.read_table_from_csv(path=self.csv_path, header=True)
        for order in self.orders_data:
            logger.info(order)
            self.browser.wait_until_page_contains_element(self.head_locator, timeout=timedelta(seconds=10))
            self.browser.select_from_list_by_value(self.head_locator, order['Head'])
            """
            What actually is group name?
            IF there is radio button, it means it contains multiple inputs so check the name attribute
              and all inputs have same name, So we can say that is group name.
            """
            self.browser.select_radio_button(group_name="body", value=order['Body'])
            self.browser.input_text(locator=self.legs_input, text=str(order['Legs']))
            self.browser.input_text(locator=self.address_input, text=order['Address'])
            self.click_on_locator(self.preview_locator)
            self.click_on_locator(self.order_btn)
            while True:
                if locator := self.find_locator(self.receipt_locator, timeout=15):
                    self.browser.click_element_when_visible(locator)
                    break
                self.click_on_locator(self.order_btn)

            self.browser.wait_until_page_contains_element(self.image_locator)
            self.browser.screenshot(self.image_locator,
                                    filename=f"{self.screenshot_path}/{order['Order number']}.png")
            receipt_html = self.browser.get_element_attribute(self.receipt_locator, attribute='innerHTML')
            self.pdf.html_to_pdf(receipt_html, f"{self.pdf_path}/{order['Order number']}.pdf")
            self.pdf.add_watermark_image_to_pdf(image_path=f"{self.screenshot_path}/{order['Order number']}.png",
                                                source_path=f"{self.pdf_path}/{order['Order number']}.pdf",
                                                output_path=f"{self.receipt_directory}/{order['Order number']}.pdf")
            self.processed_orders += 1
            # another order
            self.browser.click_button_when_visible(locator=self.another_btn)
            self.handle_pop_up()

    def start(self):
        logger.info("Process is started.")
        self.open_browser()
        self.handle_pop_up()
        self.download_orders_csv()
        self.orders_processing()

    def finish(self):
        """Release resources."""
        self.browser.close_browser()
        logger.info("Process has finished.")
