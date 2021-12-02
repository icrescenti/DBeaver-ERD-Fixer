import os
import re
import json
import platform
from os.path import exists

sources = None
osName = platform.system()

if (osName == "Windows"):
    f = open(os.getenv('APPDATA') + "\DBeaverData\workspace6\General\.dbeaver\data-sources.json", "r")
    sources = json.loads(f.read())
elif (osName == "Linux"):
    f = open(os.path.expanduser('~') + "/.local/share/DBeaverData/workspace6/General/.dbeaver/data-sources.json", "r")
    sources = json.loads(f.read())

connections = sources['connections']
f.close()

print("\nOperating System: " + osName)
print("List of connections:")
for index, connection in enumerate(connections.keys()):
    print("     " +  str(index+1) + ") " + connections[connection]['name'])

option = input()
uid = None
index = 0
connections = list(connections.keys())

while (uid == None and index < len(connections)):
    if (str(index+1) == option):
        uid=connections[index]
    index += 1

print("ERD File:")
folderPath = input()
if (exists(folderPath) == False):
    print("INVALID FILE!")
    exit()

f2 = open(folderPath, "r")
erdFile = f2.read()
erdFile = re.sub('<data-source id=\"?(.*?)\">', '<data-source id="' + uid + '">', erdFile,  flags=re.DOTALL)
f2.close()

f3 = open(folderPath, "w")
f3.write(erdFile)
f3.close()

print("Done, the ERD file was updated successfully")