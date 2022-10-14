import PySimpleGUI as sg
import os.path
import os
import platform
import json
import re

osName = platform.system()
dbeaverPath = ""

if (osName == "Windows"):
    dbeaverPath = os.getenv('APPDATA') + "\DBeaverData\workspace6\General\.dbeaver\data-sources.json"
elif (osName == "Linux"):
    dbeaverPath = os.path.expanduser('~') + "/.local/share/DBeaverData/workspace6/General/.dbeaver/data-sources.json"

f = open(dbeaverPath , "r")
sources = json.loads(f.read())
f.close()

file_list_column = [
    [
        sg.FileBrowse(key="SelectedFile"),
        sg.Text("No file selected", size=(25, 1), enable_events=True, key="SelectedFile")
    ],
    [
        sg.Text("Target database: "),
        sg.In(size=(25, 1), enable_events=True, key="DatabaseName"),
    ],
    [sg.Text("Connections: ")],
    [
        sg.Listbox(
            values=sources['connections'], enable_events=True, size=(40, 10), key="Connections"
        )
    ],
]

image_viewer_column = [
    [sg.Text("File information:")],
    [sg.Text("Detected database: none", size=(40, 1), key="DatabaseNameFromFile")],
    [sg.Text("Detected id: none", size=(40, 1), key="IdFromFile")],
    [sg.Text("Content:")],
    [sg.Text(size=(40, 15), key="TEST")],
]

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ],
    [sg.ReadButton('Done', size = (12,1))]
]

window = sg.Window("ERD Importer", layout)

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if values["SelectedFile"] != "":
        f = open(values["SelectedFile"], "r")
        erdFile = f.read()
        print(re.findall('<data-source id=\"?(.*?)\">', erdFile,  flags=re.DOTALL))
        window["DatabaseNameFromFile"].update("Detected database: " + re.findall('fq-name=\"?(.*?)\"', erdFile,  flags=re.DOTALL)[0].split('.')[0])
        window["IdFromFile"].update("Detected id: " + re.findall('<data-source id=\"?(.*?)\">', erdFile,  flags=re.DOTALL)[0])
        window["TEST"].update(erdFile[:450] + "...")
        f.close()

    if event == "Done":
        print("python3 ./ERD\ Fixer.py " + list(sources['connections'])[window["Connections"].get_indexes()[0]])
        break


window.close()