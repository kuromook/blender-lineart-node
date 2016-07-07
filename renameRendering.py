
import os
import re

path = "~/Desktop/rendering/1/"
path = os.path.expanduser(path)
os.chdir(path)
files = os.listdir(path)
while files:
    file = files.pop()
    o = re.search("([a-zA-Z_\-]+)(\d+)", file)
    # like rendering_lineart0001.png
    if o:
        name, count = o.group(1), o.group(2)
        old = name + "0001" + ".png"
        if count != "0001" and old in files:
            os.remove(old)
            os.rename(file, old)
            files.remove(old)
        elif count != "0001":
            os.rename(file, old)


