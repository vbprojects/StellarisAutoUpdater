import sys
from cleardirs import*
from resetimport import*
print("what function do you want\nadd list = al\n add single mod = a\n run mod downloader = d\n movefiles = m\n quit = q")
op = input()
op = op.strip()
if op == "q":
    sys.exit()
elif op == "al":
    os.system("python addList.py")
elif op == "a":
    os.system("python addmods.py")
elif op == "d":
    os.system("python scraper.py")
elif op == "m":
    os.system("python moveFiles.py")
elif op == "res":
    clear()
    resetl()
    os.system("python main.py")
elif op == "clearmods":
    clear()