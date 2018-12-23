import shutil
import os
import zipfile
filename = "924990631"
zipf = ""
tempdir = os.listdir("temp/"+filename)
print(tempdir)
z = zipfile.ZipFile("temp/"+filename+"/"+tempdir[0])
z.extract("descriptor.mod","modfile")
z.close()
os.rename("modfile/"+"descriptor.mod","modfile/"+filename+".mod")
shutil.move("temp/"+filename,"mods")