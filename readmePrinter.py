import time

with open("README.md") as text:
    lines = text.readlines()

    for line in lines:
        print(line)
        time.sleep(1)