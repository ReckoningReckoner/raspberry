import imp
import subprocess

try:
    modules = open("dependencies")
except FileNotFoundError:
    print("Cannot find dependencies.txt, try another git pull")

for line in modules:
    line = line.strip()
    try:
        imp.find_module(line)
        print(line, "is already installed")
    except ImportError:
        subprocess.call(["sudo", "pip3", "install", line])

print("ready to go!")
