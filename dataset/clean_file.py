import os

path = "./data"

try:
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path)
except FileNotFoundError:
    print("No file found")

print("File removed successfully")