import os
import shutil
from pathlib import Path

from dataclasses import dataclass, asdict


class Directories:
    base_directory = Path().cwd()

    output_path = base_directory / "output"
    orders_path = output_path / "orders.csv"

    screenshot_directory = output_path / "screenshot"
    pdf_directory = output_path / "pdf"
    receipt_directory = output_path / "receipt"

    @staticmethod
    def create_directory(folder_path: str):
        shutil.rmtree(folder_path, ignore_errors=True)
        try:
            os.mkdir(folder_path)
        except FileExistsError:
            ...

    @classmethod
    def generate_structure(cls):
        [cls.create_directory(str(f)) for f in
         [cls.output_path, cls.screenshot_directory, cls.pdf_directory, cls.receipt_directory]]
