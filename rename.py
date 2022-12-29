#renaming file using python
import os
import shutil
from os import path


def main():  # make a duplicate of an existing file
    if path.exists("task"):
        src = path.realpath("guru99.txt");  # rename the original file
        os.rename('task', 'career.task.txt')


if __name__ == "__main__":
    main()
