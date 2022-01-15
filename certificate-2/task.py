"""Template robot with Python."""

import os

from lazy.project import Certificate

path = F"{os.getcwd()}/output"
orders_path = f"{os.getcwd()}/orders.csv"


def run_it():
    certificate = Certificate(downloading_path=path, csv_path=orders_path)
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
        run_it()
    except Exception as e:
        print(e)
    else:
        minimal_task()
