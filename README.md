# StellarisAutoUpdater
Grabs mods from steam work shop by http://steamworkshop.download/. Autmoatically checks dates and moves files and creates valid mod files. Should work for any paradox game with the same modding structure and changing paths


To start you need python 3.6

You need to install a couple of things including

BeautifulSoup4 

pip install BeautifulSoup4

selenium

pip install selenium

clint

pip install clint

and lxml

pip install lxml


YOU NEED TO ADJUST SOME VARIABLES IN THE FILES SPECIFIED BELOW

now just run the bat file and select whatever option you want

Description of files and commands

al = addList.py = it will add to the download queue all the mods from a collections steam workshop link for example https://steamcommunity.com/workshop/filedetails/?id=1366472745

a = addmods.py = adds a single mod to the download queue for example https://steamcommunity.com/sharedfiles/filedetails/?id=1583828739

d = scraper.py = checks if links in the download queue need updating or downloading, updates needsmove

m = moveFiles.py = moves files that need moving to correct directory 

YOU NEED TO ADJUST USER VARIABLE OR PATHS IN THIS FILE (movefiles.py)

res = reset = debug tool, clears download queue (important.txt) and clears modfiles and mod dirs

fixmods.py = file that takes descriptor.mod out of mod zips and transforms it into an actual mod file needed for stellaris to identify mods in the client 

YOU NEED TO ADJUST USER VARIABLE OR PATHS IN THIS FILE (fixmods.py)

important.txt = download queue and mod list, stores mod links and date updated

needsmove = You shouldnt need to touch this ever, specifies mods that need to be moved to workship dir and stellaris mod dir

main.py = the thing the bat file runs that gives you options

runThis.bat = opens up cmd in project dir and opens up main.py (double click it)






