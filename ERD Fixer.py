import os
import re
import json
import platform
from os.path import exists

sources = None
osName = platform.system()
dbeaverPath = ""

if (osName == "Windows"):
    dbeaverPath = os.getenv('APPDATA') + "\DBeaverData\workspace6\General\.dbeaver\data-sources.json"
elif (osName == "Linux"):
    dbeaverPath = os.path.expanduser('~') + "/.local/share/DBeaverData/workspace6/General/.dbeaver/data-sources.json"

f = open(dbeaverPath , "r")
sources = json.loads(f.read())
f.close()

connections = sources['connections']

print("Operating System: " + osName)
print("List of connections:")
for index, connection in enumerate(connections.keys()):
    print("\t" +  str(index+1) + ") " + connections[connection]['name'])

option = input("> ")
uid = None
index = 0
connections = list(connections.keys())

while (int(option) > len(connections)):
    print("Incorrect connection!")
    option = input("> ")

while (uid == None and index < len(connections)):
    if (str(index+1) == option):
        uid=connections[index]
    index += 1

databaseName = input("ERD database name: ")
folderPath = input("ERD File: ")
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

sources['virtual-models'][connection][databaseName]["@properties"]["erd.diagram.state"]["serialized"] = erdFile
f4 = open(dbeaverPath , "w")
f4.write(json.dumps(sources, indent=4))
f4.close()

print("Done, the ERD file was updated successfully")