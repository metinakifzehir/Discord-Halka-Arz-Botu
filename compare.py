eskii = open("eski.txt", 'r', encoding="utf-8")
lines = []
lines2 = []
eski = []
halkarz = []
halkarzdata = ""
data = ""
for line in eskii:
    lines.append(line)
for line in lines:
    data += line
    if line == "\n":
        eski.append(data)
        data = ""
halkarzz = open("halkarz.txt", 'r', encoding="utf-8")
outfile = open("yeni.txt", 'w', encoding="utf-8")
data = ""
for line in halkarzz:
    lines2.append(line)
for line in lines2:
    data += line
    if line == "\n":
        halkarz.append(data)
        data = ""
for line in halkarz:
    if not (line in eski):
        outfile.write(line)
