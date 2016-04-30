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
    sync_directory = "backend"
    subprocess.call(["sh", sync_directory + "/" + "syncphoto.sh", directory])


def get_sorted_photos():
    photos = []
    for f in sorted(listdir(directory)):
        if f.endswith(".jpg") or f.endswith(".jpeg"):
            photos.append(f)

    return photos


def take_photo():
    filename = str(int(time.time()))
    files = get_sorted_photos()
    if len(files) > max_album_size:
        for f in files[0:len(files)-max_album_size]:
            subprocess.call(["rm", "-f", directory + "/" + f])

    subprocess.call(["fswebcam", "-r 720x480",
                     directory + "/" + filename + ".jpg"])
    sync_photo()


def get_newest_photo():
    file_names = get_sorted_photos()
    if len(file_names) == 0:
        return ""

    return "photos/" + file_names[-1]

if __name__ == "__main__":
    take_photo()
