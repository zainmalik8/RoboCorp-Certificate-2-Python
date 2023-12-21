import unittest

from config import Directories
from workflow.project import Process


class CertificateTest(unittest.TestCase):
    process = driver = None

    @classmethod
    def setUpClass(cls):
        Directories.generate_structure()
        cls.process, cls.sie_title = Process(), "RobotSpareBin Industries Inc. - Intranet"
        cls.driver = cls.process.browser
        cls.process.open_browser()

    def test010_site(self):
        self.assertEqual(self.driver.get_title(), self.sie_title)

    def test020_pop_up(self):
        self.assertTrue(self.process.handle_pop_up())

    def test030_orders_file(self):
        self.process.download_orders_csv()
        self.assertTrue(self.process.csv_path.exists())

    def test040_orders_processing(self):
        self.process.orders_processing()
        self.assertEqual(len(self.process.orders_data), self.process.processed_orders)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close_browser()


if __name__ == "__main__":
    unittest.main()
