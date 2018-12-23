import os
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

inp = input("please give a link (q to quit)")
while(inp.strip() != "q"):
    if inp.strip() not in links:
        links.append(inp.strip())
        dates.append("never")
        changes += 1
    else:
        print("link already in file")
    inp = input("please give a link (q to quit)")
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
    os.remove("important.txt")
    os.rename("temp.txt", "important.txt")
os.system("python main.py")