"""Template robot with Python."""

from workflow.project import Process

from config import Directories
from logger import logger


def task():
    process = Process()

    try:
        Directories.generate_structure()
        process.start()
    except Exception as error:
        print(error)
    finally:
        process.finish()


if __name__ == "__main__":
    logger.warning("Starting Robo-corp certificate-2")
    task()
    logger.warning("Robo-corp certificate-2 is completed.")
