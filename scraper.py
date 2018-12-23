from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
from selenium.webdriver.chrome.options import Options
import requests, zipfile
import re
import shutil
from clint.textui import progress
from fixmods import fixmods
import sys

def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

modfiledir = os.listdir("modfile")
# for x in modfiledir:
#     os.remove("modfile/"+x)
# modsdir = os.listdir("mods")
# for x in modsdir:
#     temps = os.listdir("mods/"+x)
#     for y in temps:
#         os.remove("mods/"+x+"/"+y)
#     os.rmdir("mods/"+x)
options = Options()
options.add_experimental_option("prefs", {
  "download.default_directory": r"C:\Users\xxx\downloads\Test",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})
#by https://gist.github.com/ergoithz
def xpath_soup(element):
    """
    Generate xpath from BeautifulSoup4 element
    :param element: BeautifulSoup4 element.
    :type element: bs4.element.Tag or bs4.element.NavigableString
    :return: xpath as string
    :rtype: str

    Usage:

    >>> import bs4
    >>> html = (
    ...     '<html><head><title>title</title></head>'
    ...     '<body><p>p <i>1</i></p><p>p <i>2</i></p></body></html>'
    ...     )
    >>> soup = bs4.BeautifulSoup(html, 'html.parser')
    >>> xpath_soup(soup.html.body.p.i)
    '/html/body/p[1]/i'
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        """
        @type parent: bs4.element.Tag
        """
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if siblings == [child] else
            '%s[%d]' % (child.name, 1 + siblings.index(child))
        )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

f = open("important.txt")
print("generating lists")
links = []
dates = []
s = f.readline().strip()
print(s)

while s != "dates":
    if s == 'dates':
        #print("reached here")
        break
    links.append(s)
    s = f.readline().strip()
s = f.readline().strip()
print("generated links list")
while s != "end":
    if s == 'end':
        break
    #print(s)
    dates.append(s)
    s=f.readline().strip()
print("generated lists")
# driver = webdriver.Firefox(firefox_profile= fp , executable_path=r'geckodriver.exe')
#driver = webdriver.Firefox(executable_path=r"geckodriver.exe")
driver = webdriver.Edge("MicrosoftWebDriver.exe")
#driver = webdriver.PhantomJS("phantomjs-2.1.1-windows/bin/phantomjs.exe")
needsupdate = 0
i = 0
needmove = []
for l in links:
    sucup = False
    driver.get(l)
    soup = BeautifulSoup(driver.page_source,features="lxml")
    rightcontainer = soup.find_all("div",{"class":"detailsStatRight"})
    cur = ""
    try:
        cur = rightcontainer[2].string[0:rightcontainer[2].string.index('@')]
    except:
        cur = rightcontainer[1].string[0:rightcontainer[1].string.index('@')]
    print(dates[i])
    print(cur)
    try:
        if dates[i].strip() != cur.strip():
            needsupdate+=1
            print("updating "+l)
            driver.get("http://steamworkshop.download/")
            soup = BeautifulSoup(driver.page_source, features="lxml")
            searchbox = soup.find("input",{"class":"textbox"})
            searchbox = driver.find_element_by_xpath(xpath_soup(searchbox))
            searchbox.send_keys(l+"\n")
            buttonhit = False
            timeout = 0
            while not buttonhit:
                try:
                    soup = BeautifulSoup(driver.page_source,features="lxml")
                    button = soup.find("input",{"id":"steamdownload"})
                    button = driver.find_element_by_xpath(xpath_soup(button))
                    button.click()
                    buttonhit = True
                except Exception:
                    if timeout == 20:
                        raise ValueError("button did not init in 4 seconds skipping file")
                    time.sleep(.2)
            print("got first button")
            buttonhit = False
            url = ""
            result = ""
            soup = ""
            found = False
            timeout = 0
            while not buttonhit:
                try:
                    soup = BeautifulSoup(driver.page_source,features="lxml")
                    result = soup.find("div",{"id":"result"})
                    if str(result).find("Error") != -1:
                        buttonhit = True
                        print("could not download " + l)
                    #print(result)
                    soup = BeautifulSoup(str(result),features="lxml")
                    #print(result)
                    result = soup.find("a")
                    #print(result)
                    #print(result)
                    url = result["href"]
                    buttonhit = True
                    found = True
                except AttributeError:
                    if timeout == 20:
                        raise ValueError("button did not init in 4 seconds skipping file")
                    time.sleep(.2)
                except KeyError:
                    if timeout == 20:
                        raise ValueError("button did not init in 4 seconds skipping file")
                    #print("pre not init")
                    time.sleep(.2)
                except TypeError:
                    if timeout == 20:
                        raise ValueError("button did not init in 4 seconds skipping file")
                    #print("result not init")
                    time.sleep(.2)
            print("got second button")
            if(found):
                filename = result.string[:len(result.string) - 4]
                r = requests.get(url, stream=True)
                path = filename+".zip"
                with open(path, 'wb') as f:
                    total_length = int(r.headers.get('content-length'))
                    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
                        if chunk:
                            f.write(chunk)
                            f.flush()

                #print(filename)
                z = zipfile.ZipFile(filename+".zip")
                z.extractall("temp")
                z.close()
                os.remove(filename+".zip")
                needmove.append(filename)
                zipf = ""
                tempdir = os.listdir("temp/" + filename)
                #print(tempdir)
                z = zipfile.ZipFile("temp/" + filename + "/" + tempdir[0])
                z.extract("descriptor.mod", "modfile")
                z.close()
                modfiledir = os.listdir("modfile")
                if filename + ".mod" in modfiledir:
                    os.remove("modfile/" + filename + ".mod")
                os.rename("modfile/" + "descriptor.mod", "modfile/" + filename + ".mod")
                fixmods(filename)
                modsdir = os.listdir("mods")
                if filename in modsdir:
                    for x in os.listdir("mods/"+filename):
                        os.remove("mods/"+filename+"/"+x)
                    os.rmdir("mods/"+filename)
                shutil.move("temp/" + filename, "mods")
                sucup = True
    except Exception as e:
        print(e)
        print("skipping this file")
    if sucup:
        dates[i] = cur
        print(l+" is up to date")
    else:
        print(l+" could not download try again later")
    i+=1
if needsupdate != 0:
    newf = open("temp.txt","w+")
    for x in links:
        newf.write(x+"\n")
    newf.write("dates\n")
    for x in dates:
        newf.write(x+"\n")
    newf.write("end\n")
    f.close()
    newf.close()
    n = open("needsmove","w+")
    print(needmove)
    for x in needmove:
        n.write(x+"\n")
    n.close()
    try:
        os.remove("important.txt")
        os.rename("temp.txt","important.txt")
    except Exception:
        print("it seems like you have either temp.txt or important.txt open, the file update happened but the file list has not been updated, delete important.txt and rename temp.txt to important.txt if you want things to work")
print("end of updater")
driver.quit()
os.system("python main.py")
