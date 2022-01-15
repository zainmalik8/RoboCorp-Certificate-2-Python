"""Template robot with Python."""

import os

from lazy.project import Certificate

base_directory = os.getcwd()

download_path = F"{base_directory}/output"

screenshot_directory = f'{download_path}/screenshot'
pdf_directory = f'{download_path}/pdf'
receipt_direc = f"{download_path}/receipt"

orders_path = f"{base_directory}/orders.csv"


def paths():

    if os.path.exists(screenshot_directory) or os.path.exists(pdf_directory) or os.path.exists(receipt_direc):
        pass
    else:
        os.mkdir(screenshot_directory)
        os.mkdir(pdf_directory)
        os.mkdir(receipt_direc)


def run_it():
    certificate = Certificate(downloading_path=download_path, csv_path=orders_path,
                              screenshot_path=screenshot_directory, pdf_path=pdf_directory,
                              receipt_directory=receipt_direc)
    try:
        certificate.download_directory()
        certificate.open_browser()
        certificate.click_ok()
        certificate.download_orders_csv()
        certificate.orders()
    finally:
        'later on'


def minimal_task():
    print("Done.")


if __name__ == "__main__":
    try:
        paths()
        run_it()
    except Exception as e:
        print(e)
    else:
        minimal_task()
