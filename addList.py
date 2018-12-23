import os
from bs4 import BeautifulSoup
from selenium import webdriver
import time
f = open("important.txt")
print("generating lists")
links = []
dates = []
s = f.readline().strip()
print(s)

while s != "dates":
    if s == 'dates':
        print("reached here")
        break
    links.append(s)
    s = f.readline().strip()
s = f.readline().strip()
changes = 0
print("generated links list")
while s != "end":
    if s == 'end':
        break
    print(s)
    dates.append(s)
    s=f.readline().strip()

print("generated lists")
driver = webdriver.Edge("MicrosoftWebDriver.exe")
inp = input("please give a link (q to quit)")
driver.get(inp.strip())
soup = BeautifulSoup(driver.page_source,features="lxml")
temp = soup.find("div",{"class":"collectionChildren"})
soup = BeautifulSoup(str(temp),features="lxml")
a = soup.find_all("a")

for x in a:
    try:
        if x["href"].strip() not in links:
            if x["href"].find("profiles") == -1 and x["href"].find("sharedfiles") != -1 and x["href"].find("linkfilter") == -1:
                links.append(x["href"].strip())
                dates.append("never")
                print(x["href"] + "added")
                changes += 1
        else:
            print("link already in file or otherwise invalid (ignore)")
    except KeyError:
        print("caught a button (ignore)")
    except AttributeError:
        print("caught a button (ignore)")
if changes != 0:
    newf = open("temp.txt", "w+")
    for x in links:
        newf.write(x + "\n")
    newf.write("dates\n")
    for x in dates:
        newf.write(x + "\n")
    newf.write("end\n")
    f.close()
    newf.close()
    time.sleep(.5)
    try:
        os.remove("important.txt")
        os.rename("temp.txt","important.txt")
    except Exception:
        print("it seems like you have either temp.txt or important.txt open, the file update happened but the file list has not been updated, delete important.txt and rename temp.txt to important.txt if you want things to work")
driver.quit()
os.system("python main.py")