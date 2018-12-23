import os
user = "Alterix"
workshop = "C:/Users/"+user+"/Documents/Paradox Interactive/Stellaris/workshop/content/281990"

try:
    os.listdir(workshop)
except FileNotFoundError:
    print("either you did not adjust path or the path is wrong, input user name here")
    user = input()
def fixmods(s:str):
    f = open("modfile/"+s+".mod")
    temp = open("temp/"+s+".mod","w+")
    temp.write(f.readline())
    line = f.readline()
    line = line.strip()
    name = line[line.index("=")+2:len(line)]
    path = "path=\""+workshop+"/"+s+"/"+name+"\n"
    print(path)
    temp.write(path)
    line = f.readline()
    while line != "":
        temp.write(line)
        line = f.readline()
    f.close()
    temp.close()
    os.remove("modfile/"+s+".mod")
    os.rename("temp/"+s+".mod","modfile/"+s+".mod")
