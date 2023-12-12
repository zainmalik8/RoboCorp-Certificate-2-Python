"""Template robot with Python."""

from workflow.project import Process

from config import Directories


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
    task()
