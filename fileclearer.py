import os
modfiledir = os.listdir("modfile")
for x in modfiledir:
    os.remove("modfile/"+x)
modsdir = os.listdir("mods")
for x in modsdir:
    temps = os.listdir("mods/"+x)
    for y in temps:
        os.remove("mods/"+x+"/"+y)
    os.rmdir("mods/"+x)