import os
import shutil
user = "Alterix"
modfiledir = ""
modfileprime = os.listdir()
try:
    modfiledir = "C:/Users/"+user+"/Documents/Paradox Interactive/Stellaris/mod"
    modfileprime = os.listdir(modfiledir)
except FileNotFoundError:
    print("either you did not adjust path or the path is wrong, input user name here")
    user = input()
    modfiledir = "C:/Users/" + user + "/Documents/Paradox Interactive/Stellaris/mod"
    modfileprime = os.listdir(modfiledir)
workshop = "C:/Users/"+user+"/Documents/Paradox Interactive/Stellaris/workshop/content/281990"
modfiles = os.listdir("modfile")
modss = os.listdir("mods")
modsprime = os.listdir(workshop)
print("generating lists")
needmove = []
f = open("needsmove")
line = f.readline()
while(line.strip() != ""):
    needmove.append(line.strip())
    line = f.readline()
for x in needmove:
    if x.strip() in modfileprime:
        os.remove(modfiledir+"/"+x)
    shutil.copy("modfile/"+x+".mod",modfiledir)
for x in needmove:
    if x.strip() in modsprime:
        tempdir = os.listdir(workshop+"/"+x.strip())
        for y in tempdir:
            os.remove(workshop+"/"+x.strip()+"/"+y.strip())
        os.rmdir(workshop + "/" + x.strip())
    ks = os.listdir("mods/"+x.strip())
    os.mkdir(workshop + "/" + x.strip())
    for k in ks:
        shutil.copy("mods/" + x.strip()+"/"+k.strip(), workshop+"/"+x.strip())
f.close()
f = open("needsmove","w+")
f.close()
os.system("python main.py")