import subprocess
import time
import os
from os import listdir
import sys

directory = "static/photos"
max_album_size = 20

if __debug__:
    if not os.path.isdir(directory):
        subprocess.call(["mkdir", directory])

    try:
        subprocess.check_output(["which", "fswebcam"])
    except subprocess.CalledProcessError:
        print("Error, fswebcam not installed")
        print("Exiting program")
        sys.exit(1)


def sync_photo():
    subprocess.call(["sh", directory + "/" + "syncphoto.sh", directory])


def take_photo():
    filename = str(int(time.time()))
    files = sorted(listdir(directory))
    if len(files) > max_album_size:
        for f in files[0:len(files)-max_album_size]:
            subprocess.call(["rm", directory + "/" + f])

    subprocess.call(["fswebcam", "-r 720x480",
                     directory + "/" + filename + ".jpg"])
    sync_photo()


def get_newest_photo():
    file_names = sorted(listdir(directory))
    if len(file_names) == 0:
        return ""

    return "photos/" + file_names[-1]

if __name__ == "__main__":
    sync_photo()
