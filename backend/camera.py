import subprocess
import time
from os import listdir

directory = "photos"
filename = str(int(time.time()))
max_album_size = 20

def take_photo():
    files = listdir(directory)
    if len(files) > max_album_size:
        for f in files[0:len(files)-max_album_size]:
            subprocess.call(["rm", directory + "/" + f])

    subprocess.call(["fswebcam", directory + "/" + filename + ".jpg"])

if __name__ == "__main__":
    take_photo()
